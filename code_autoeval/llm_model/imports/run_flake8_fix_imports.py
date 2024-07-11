"""Run Flake8 and fix imports."""

import os
import subprocess
import tempfile
from typing import Any, Dict, List, Optional, Set, Tuple

from multiuse.model import class_data_model

from code_autoeval.llm_model.utils.validation import validate_code


class RunFlake8FixImports:
    """Run Flake8, find, and fix import errors in the code."""

    @classmethod
    @validate_code()
    def run_flake8_pipeline_with_temp_file(
        cls,
        code: str,
        class_model: class_data_model.ClassDataModel,
        original_imports: Dict[str, str],
        unique_project_imports: Optional[Dict[str, str]],
        **kwargs,  # Need the kwargs for validate_code
    ) -> Tuple[str, bool]:
        """Create a temporary file with the code."""
        instance = cls()

        # Create a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        try:
            return instance.run_flake_fix_imports(
                temp_file_path,
                code,
                class_model=class_model,
                original_imports=original_imports,
                unique_project_imports=unique_project_imports,
            )
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)

    @classmethod
    def run_flake_fix_imports(
        cls,
        temp_file_path: str,
        code: str,
        class_model: class_data_model.ClassDataModel,
        original_imports: Dict[str, str],
        unique_project_imports: Optional[Dict[str, str]],
    ) -> Tuple[str, bool]:
        """Run flake8 and fix import errors."""
        self = cls()

        flake8_result = self.run_flake8_against_code(temp_file_path)

        problematic_lines, undefined_names = self.parse_flake8_output(flake8_result)

        # Remove class definition from the file
        import_lines_to_add, undefined_names = self.remove_class_definition_from_file(
            import_lines_to_add=[],
            undefined_names=undefined_names,
            code=code,
            class_model=class_model,
        )

        # Add to import lines from the original imports
        import_lines_to_add, remaining_undefined = (
            self.add_to_import_lines_from_original_imports(
                import_lines_to_add=import_lines_to_add,
                original_imports=original_imports,
                undefined_names=undefined_names,
            )
        )

        # Fix remaining import statements
        import_lines_to_add, remaining_undefined = self.fix_remaining_import_statements(
            import_lines_to_add=import_lines_to_add,
            remaining_undefined=remaining_undefined,
            unique_imports_dict=unique_project_imports,
        )

        if not import_lines_to_add:
            return code, False

        if remaining_undefined:
            raise ImportError(
                f"Unresolved import errors for: {', '.join(remaining_undefined)}"
            )

        # Combine new import lines
        processed_code = self.combine_new_import_lines(
            import_lines_to_add=import_lines_to_add,
            code=code,
            class_model=class_model,
        )

        return processed_code, True

    def run_flake8_against_code(
        self, temp_file_path: str
    ) -> subprocess.CompletedProcess:
        """Run flake8 against the code."""
        return subprocess.run(
            ["flake8", "--select=E999,F401,F821,F822,F823,F841,E501", temp_file_path],
            capture_output=True,
            text=True,
        )

    def parse_flake8_output(
        self,
        flake8_output: subprocess.CompletedProcess[str],
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

    def remove_class_definition_from_file(
        self,
        import_lines_to_add: List[str],
        undefined_names: Set[Any],
        code: str,
        class_model: class_data_model.ClassDataModel,
    ) -> Tuple[List[str], Set[Any]]:
        """Remove the class definition from the file."""
        # Remove duplicate import errors
        import_lines_to_add = []
        # If the import error is related to the class that was supposed to be
        # imported, then use the class_model path to import the class
        # for i, error in enumerate(import_errors):
        if class_model and (
            class_model.class_name in undefined_names
            or f"import {class_model.class_name}" not in code
        ):
            module_relative_path = (
                str(class_model.module_relative_path)
                .replace("/", ".")
                .replace(".py", "")
            )

            # Then add the absolute import line to the code.
            import_lines_to_add.append(
                f"from {module_relative_path} import {class_model.class_name}"
            )
            if class_model.class_name in undefined_names:
                # And then remove the error from the list
                undefined_names.remove(class_model.class_name)

        return import_lines_to_add, undefined_names

    def add_to_import_lines_from_original_imports(
        self,
        import_lines_to_add: List[str],
        original_imports: Dict[str, str],
        undefined_names: Set[Any],
    ) -> Tuple[List[str], Set[Any]]:
        """Add to the import lines from the original imports."""
        import_lines_to_add.extend(
            original_imports[name]
            for name in undefined_names
            if name in original_imports
        )

        # Raise an error if there are still import issues
        remaining_undefined = undefined_names - set(import_lines_to_add)

        return import_lines_to_add, remaining_undefined

    def fix_remaining_import_statements(
        self,
        import_lines_to_add: List[str],
        remaining_undefined: Set[Any],
        unique_imports_dict: Dict[str, str],
    ) -> Tuple[List[str], Set[Any]]:
        # If these are known modules that have import paths within the project
        # then we can add them to the import_lines_to_add
        # and remove them from the remaining_undefined
        # This is to avoid adding unnecessary imports to the code
        # and to avoid raising an error for known imports

        for name in list(remaining_undefined):
            if name in unique_imports_dict:
                import_lines_to_add.append(unique_imports_dict[name])
                remaining_undefined.remove(name)
            if name in {"MagicMock", "patch", "AsyncMock"}:
                import_lines_to_add.append(f"from unittest.mock import {name}")
                remaining_undefined.remove(name)
            if name in {"tmp_path", "capsys", "caplog"}:
                import_lines_to_add.append(f"from pytest import {name}")
                remaining_undefined.remove(name)

        return import_lines_to_add, remaining_undefined

    def combine_new_import_lines(
        self,
        import_lines_to_add: List[str],
        code: str,
        class_model: class_data_model.ClassDataModel,
    ) -> str:
        """Combine the new import lines."""
        # Process the code
        processed_lines = import_lines_to_add + code.splitlines()
        processed_code = "\n".join(processed_lines)

        if f"import {class_model.class_name}" not in processed_code:
            raise ImportError(
                f"Import statement - import {class_model.class_name} not found in the code after preprocessing"
            )

        return processed_code
