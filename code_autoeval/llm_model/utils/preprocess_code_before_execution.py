"""Class for preprocessing code before execution."""

import os
import re
import subprocess
import tempfile
from typing import Dict, Optional, Tuple

from code_autoeval.llm_model.utils.code_cleaning.run_pyflakes_isort import (
    RunPyflakesIsort,
)
from code_autoeval.llm_model.utils.extraction.extract_classes_from_file import (
    PythonClassManager,
)
from code_autoeval.llm_model.utils.extraction.extract_imports_from_file import (
    ExtractImportsFromFile,
)
from code_autoeval.llm_model.utils.model import function_attributes
from code_autoeval.llm_model.utils.model.class_data_model import ClassDataModel
from code_autoeval.llm_model.utils.validation.validate_regexes import (
    ValidateRegexes,
    validate_code,
)


class PreProcessCodeBeforeExecution(
    ValidateRegexes, RunPyflakesIsort, ExtractImportsFromFile
):

    @validate_code()
    def run_preprocess_pipeline(
        self,
        code: str,
        max_line_length: int = 120,
        class_model: Optional[ClassDataModel] = None,
        func_attributes: function_attributes.FunctionAttributes = None,
        is_pytest_format: bool = False,
        **kwargs,
    ) -> str:
        code = self.remove_non_code_patterns(code)

        code, was_modified = self.preprocess_code(
            code,
            max_line_length=max_line_length,
            class_model=class_model,
            func_attributes=func_attributes,
            is_pytest_format=is_pytest_format,
            **kwargs,
        )

        if was_modified:
            code, was_modified = self.preprocess_code(
                code, max_line_length=max_line_length, class_model=class_model, **kwargs
            )
        if was_modified:
            raise ValueError("Code was modified twice during preprocessing")

        self._log_code(code, "Code before pyflakes + isort: ")

        code, was_modified = self.run_pyflakes_isort_pipeline(
            code, max_line_length=max_line_length, class_model=class_model, **kwargs
        )

        return code

    @validate_code()
    def preprocess_code(
        self,
        code: str,
        class_model: Optional[ClassDataModel] = None,
        func_attributes: function_attributes.FunctionAttributes = None,
        is_pytest_format: bool = False,
        **kwargs,
    ) -> Tuple[str, bool]:
        """Preprocess the code before running it."""
        original_code = self._read_in_original_code(func_attributes)
        # Extract imports from the original file
        original_imports = self.extract_imports(original_code)
        # Create a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

            if kwargs.get("code_type", "") == "pytest" or is_pytest_format:
                # Then verify that we don't have the class definition in the test file.
                # the class definition would be provided by the class_model
                code = PythonClassManager.extract_remove_class_from_file(
                    class_model.class_name,
                    file_path=str(func_attributes.test_absolute_file_path),
                    content=code,
                )

        try:
            return self._extracted_from_preprocess_code_(
                temp_file_path,
                code,
                class_model=class_model,
                original_imports=original_imports,
            )
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)

    def _read_in_original_code(
        self, func_attributes: function_attributes.FunctionAttributes
    ) -> str:
        with open(func_attributes.module_absolute_path, "r") as file:
            original_code = file.read()

        self._log_code(
            str(func_attributes.module_absolute_path), "Original code file path:"
        )
        self._log_code(original_code, "Original code:")

        return original_code

    # TODO Rename this here and in `preprocess_code`
    def _extracted_from_preprocess_code_(
        self,
        temp_file_path: str,
        code: str,
        class_model: Optional[ClassDataModel] = None,
        original_imports: Dict[str, str] = None,
    ) -> Tuple[str, bool]:
        was_modified = False
        # Run flake8 on the entire file
        flake8_result = subprocess.run(
            ["flake8", "--select=E999,F401,F821,F822,F823,F841,E501", temp_file_path],
            capture_output=True,
            text=True,
        )

        # Process the flake8 output
        # problematic_lines, import_errors, undefined_names
        problematic_lines, undefined_names = self.parse_flake8_output(flake8_result)

        if problematic_lines:
            self._log_code(str(problematic_lines), "Problematic lines:")

        # Remove duplicate import errors
        import_lines_to_add = []
        # If the import error is related to the class that was supposed to be
        # imported, then use the class_model path to import the class
        # for i, error in enumerate(import_errors):
        if class_model and class_model.class_name in undefined_names:
            # Then add the absolute import line to the code.
            import_lines_to_add.append(
                f"from {class_model.module_relative_path} import {class_model.class_name}"
            )
            # And then remove the error from the list
            undefined_names.remove(class_model.class_name)

        # Add missing imports from the original file
        import_lines_to_add.extend(
            original_imports[name]
            for name in undefined_names
            if name in original_imports
        )
        # Raise an error if there are still import issues
        remaining_undefined = undefined_names - set(import_lines_to_add)

        # If these are known modules that have import paths within the project
        # then we can add them to the import_lines_to_add
        # and remove them from the remaining_undefined
        # This is to avoid adding unnecessary imports to the code
        # and to avoid raising an error for known imports

        for name in list(remaining_undefined):
            if name in self.unique_imports_dict:
                import_lines_to_add.append(self.unique_imports_dict[name])
                remaining_undefined.remove(name)
            if name in {"MagicMock", "patch", "AsyncMock"}:
                import_lines_to_add.append(f"from unittest.mock import {name}")
                remaining_undefined.remove(name)
            if name in {"tmp_path", "capsys", "caplog"}:
                import_lines_to_add.append(f"from pytest import {name}")
                remaining_undefined.remove(name)

        if remaining_undefined:
            raise ImportError(
                f"Unresolved import errors for: {', '.join(remaining_undefined)}"
            )

        if not import_lines_to_add:
            return code, was_modified

        # Process the code
        processed_lines = import_lines_to_add + code.splitlines()
        return "\n".join(processed_lines), True

    def parse_flake8_output(
        self, flake8_output: subprocess.CompletedProcess[str]
    ) -> Tuple[set, set]:
        problematic_lines = set()
        undefined_names = set()

        for line in flake8_output.stdout.splitlines():
            parts = line.split(":")
            if len(parts) >= 4:
                line_num = int(parts[1])
                error_code = parts[3].strip().split()[0]
                if error_code in ["F401", "F821"]:
                    if "undefined name" in line:
                        undefined_name = (
                            line.split("undefined name")[-1]
                            .strip()
                            .strip("'")
                            .strip('"')
                        )
                        if len(undefined_name) > 2:
                            undefined_names.add(undefined_name)
                    elif "imported but unused" not in line:
                        problematic_lines.add(line_num)

        return problematic_lines, undefined_names

    @validate_code()
    def remove_non_code_patterns(self, code: str, **kwargs) -> str:
        # Remove markdown code blocks if present
        # Split code on either ```python or ``` to remove the markdown code block
        # And keep just the code part
        code = re.split(r"```python", code, maxsplit=1)[-1]
        code = re.split(r"```", code, maxsplit=1)[0]

        code = re.sub(r"```|,$", "", code)
        # Remove leading/trailing whitespace
        return code.strip()
