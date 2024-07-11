"""Class for preprocessing code before execution."""

import re
from typing import Optional, Tuple

from multiuse.model import class_data_model

from code_autoeval.llm_model import imports

from code_autoeval.llm_model.utils import model, extraction, code_cleaning, validation
# import flake8


class PreProcessCodeBeforeExec(
    validation.ValidateRegexes,
    code_cleaning.RunPyflakesIsort,
    imports.ExtractImportsFromFile,
    imports.RunFlake8FixImports,
):

    @validation.validate_code()
    def run_preprocess_pipeline(
        self,
        code: str,
        max_line_length: int = 120,
        class_model: Optional[class_data_model.ClassDataModel] = None,
        func_attributes: model.FunctionAttributes = None,
        is_pytest_format: bool = False,
        **kwargs,
    ) -> str:
        code = self.remove_non_code_patterns(code, is_pytest_format)

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
                code,
                max_line_length=max_line_length,
                class_model=class_model,
                func_attributes=func_attributes,
                **kwargs,
            )
        if was_modified:
            raise ValueError("Code was modified twice during preprocessing")

        self._log_code(code, "Code before pyflakes + isort: ")

        code, was_modified = self.run_pyflakes_isort_pipeline(
            code, max_line_length=max_line_length, class_model=class_model, **kwargs
        )

        return code

    @validation.validate_code()
    def preprocess_code(
        self,
        code: str,
        class_model: Optional[class_data_model.ClassDataModel] = None,
        func_attributes: model.FunctionAttributes = None,
        is_pytest_format: bool = False,
        **kwargs,
    ) -> Tuple[str, bool]:
        """Preprocess the code before running it."""
        original_code, original_imports = self.find_original_code_and_imports(
            func_attributes
        )

        if is_pytest_format:
            # Then verify that we don't have the class definition in the test file.
            # the class definition would be provided by the class_model
            code = extraction.PythonClassManager.extract_remove_class_from_file(
                class_model.class_name,
                file_path=str(func_attributes.test_absolute_file_path),
                content=code,
            )

        return self.run_flake8_pipeline_with_temp_file(
            code, class_model=class_model, original_imports=original_imports, **kwargs
        )

    @validation.validate_code()
    def remove_non_code_patterns(
        self, code: str, is_pytest_format: bool = False, **kwargs
    ) -> str:
        """Remove non-code patterns from the code."""
        if is_pytest_format:
            return code
        # Remove markdown code blocks if present
        # Split code on either ```python or ``` to remove the markdown code block
        # And keep just the code part
        code = re.split(r"```python", code, maxsplit=1)[-1]
        code = re.split(r"```", code, maxsplit=1)[0]

        code = re.sub(r"```|,$", "", code)
        # Remove leading/trailing whitespace
        return code.strip()
