"""Class for preprocessing code before execution."""

import os
import re
import subprocess
import tempfile
from typing import Dict, List, Optional, Tuple

import black

from code_autoeval.clients.llm_model.utils.extraction.extract_imports_from_file import (
    ExtractImportsFromFile,
)
from code_autoeval.clients.llm_model.utils.file_path_functions import FilePathFunctions
from code_autoeval.clients.llm_model.utils.model.class_data_model import ClassDataModel
from code_autoeval.clients.llm_model.utils.code_cleaning.run_pyflakes_isort import RunPyflakesIsort
from code_autoeval.clients.llm_model.utils.validation.validate_regexes import (
    ValidateRegexes,
    validate_code,
)


class PreProcessCodeBeforeExecution(
    FilePathFunctions, ValidateRegexes, RunPyflakesIsort, ExtractImportsFromFile
):

    @validate_code()
    def run_preprocess_pipeline(
        self,
        code: str,
        max_line_length: int = 120,
        class_model: Optional[ClassDataModel] = None,
        is_pytest_format: bool = False,
        **kwargs,
    ) -> str:
        code = self.remove_non_code_patterns(code)

        if kwargs.get("code_type", "") == "pytest" or is_pytest_format:
            # Then verify that we don't have the class definition in the test file.
            # the class definition would be provided by the class_model
            # class_name = class_model.class_name.split(".")[-1]
            # code = self.wrap_remove_class_definition(code, class_name)
            pass

        code, was_modified = self.preprocess_code(
            code, max_line_length=max_line_length, class_model=class_model, **kwargs
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
        max_line_length: int = 480,
        class_model: Optional[ClassDataModel] = None,
        **kwargs,
    ) -> Tuple[str, bool]:

        # Read code from original file:
        relative_path = (class_model.absolute_path.rsplit(".", maxsplit=1)[0]).replace(
            ".", "/"
        )

        # Attach to the project root
        code_filepath = self.common.project_root.joinpath(relative_path).with_suffix(
            ".py"
        )
        with open(code_filepath, "r") as file:
            original_code = file.read()

        self._log_code(str(code_filepath), "Original code file path:")
        self._log_code(original_code, "Original code:")

        # Extract imports from the original file
        original_imports = self.extract_imports(original_code)
        # Create a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        try:
            return self._extracted_from_preprocess_code_(
                temp_file_path,
                code,
                max_line_length,
                class_model=class_model,
                original_imports=original_imports,
            )
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)

    # TODO Rename this here and in `preprocess_code`
    def _extracted_from_preprocess_code_(
        self,
        temp_file_path,
        code,
        max_line_length,
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

        # Remove duplicate import errors
        import_lines_to_add = []
        # If the import error is related to the class that was supposed to be
        # imported, then use the class_model path to import the class
        # for i, error in enumerate(import_errors):
        if class_model and class_model.class_name in undefined_names:

            absolute_path = class_model.absolute_path.rsplit(".", maxsplit=1)[0]
            # Then add the absolute import line to the code.
            import_line_to_add = f"from {absolute_path} import {class_model.class_name}"
            import_lines_to_add.append(import_line_to_add)
            # And then remove the error from the list
            # import_errors.pop(i)
            undefined_names.remove(class_model.class_name)

        # Add missing imports from the original file
        import_lines_to_add.extend(
            original_imports[name]
            for name in undefined_names
            if name in original_imports
        )
        # Raise an error if there are still import issues
        remaining_undefined = undefined_names - set(
            name for name in import_lines_to_add
        )
        if remaining_undefined:
            raise ImportError(
                f"Unresolved import errors for: {', '.join(remaining_undefined)}"
            )

        if problematic_lines:
            self._log_code(str(problematic_lines), "Problematic lines:")

        # Process the code
        lines = code.splitlines()
        # processed_lines = [
        #    line
        #    for i, line in enumerate(lines, 1)
        #    if i not in problematic_lines and len(line) <= max_line_length
        # ]

        if import_lines_to_add:
            processed_lines = import_lines_to_add + lines
            was_modified = True
        else:
            processed_lines = lines

        return "\n".join(processed_lines), was_modified

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

    def split_main_and_example(self, code: str) -> Tuple[str, str]:
        parts = code.split('if __name__ == "__main__":')
        if len(parts) == 2:
            return parts[0].strip(), f'if __name__ == "__main__":{parts[1]}'
        return code, ""

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

    @validate_code()
    def format_code_with_black(self, code: str, **kwargs) -> str:
        """Format the code using Black, removing lines with triple backticks if necessary."""
        lines = code.split("\n")
        cleaned_lines = self._remove_problematic_lines(lines)

        try:
            lines = self._ensure_double_quotes("\n".join(cleaned_lines))
            return black.format_str(lines, mode=black.FileMode())
        except black.InvalidInput as e:
            # If Black still can't format the code, return the cleaned but unformatted code
            print(f"Warning: Black couldn't format the code. Error: {e}")
            return code

    def _remove_problematic_lines(self, lines: List[str]) -> List[str]:
        """Remove lines containing triple backticks."""
        return [line for line in lines if "`" not in line]

    def _ensure_double_quotes(self, code: str) -> str:
        """Ensure the entire code block is wrapped in double quotes, preserving internal quotes."""
        # Remove leading/trailing whitespace
        code = code.strip()

        # Escape any existing double quotes in the code
        code = code.replace('"', '\\"')

        return f'"""\n{code}\n"""'

    @validate_code()
    def _format_code_with_black(self, code: str, **kwargs) -> str:
        """Format the code using Black, removing problematic lines if necessary."""
        lines = code.split("\n")
        while lines:
            try:
                return black.format_str("\n".join(lines), mode=black.FileMode())
            except black.InvalidInput as e:
                if match := re.search(r"Cannot parse: (\d+):(\d+):", str(e)):
                    line_num = int(match[1]) - 1
                    if 0 <= line_num < len(lines):
                        # Comment out the problematic line
                        lines[line_num] = (
                            f"# REMOVED DUE TO PARSING ERROR: {lines[line_num]}"
                        )
                    else:
                        self._log_code(str(lines[-1]), "Removing line:")
                        # If we can't identify the specific line, remove the last line
                        lines.pop()
                else:
                    self._log_code(str(lines[-1]), "Removing line:")
                    # If we can't parse the error message, remove the last line
                    lines.pop()

        # If we've removed all lines, return an empty string
        if not lines:
            raise ValueError("All lines were removed during formatting")

        return black.format_str("\n".join(lines), mode=black.FileMode())

    def __remove_class_definition(self, code: str, class_name: str) -> str:
        pattern = (
            r"class\s+"
            + re.escape(class_name)
            + r"\s*(?:\([^)]*\))?\s*:\s*"  # Match class inheritance if present
            r"(?:(?!^\S)[\s\S])*?"  # Match all indented lines
            r"(?=^\S|\Z)"  # Stop at the first unindented line or end of string
        )
        return re.sub(pattern, "", code, flags=re.MULTILINE)

    def wrap_remove_class_definition(self, code: str, class_name: str) -> str:
        # Then verify that we don't have the class definition in the test file.
        # the class definition would be provided by the class_model
        self._log_code(class_name, "Class name: ")

        if f"class {class_name}" in code:
            # Remove actual class definition
            code = self.remove_class_definition(code, class_name)

            # Check if there's still a class definition (which might be a patched recreation)
            remaining_class_def = re.search(
                rf"\s*class\s+{re.escape(class_name)}\s*(\([^)]*\))?\s*:", code
            )
            if remaining_class_def:
                # If it's within a patch or mock context, it's okay
                patch_context = re.search(
                    rf"(@patch|mock\.patch|with\s+patch)[^\n]*\n\s*class\s+{re.escape(class_name)}",
                    code,
                )
                if not patch_context:
                    raise ValueError(
                        f"Unexpected class definition for {class_name} found in the pytest tests."
                    )

        if f"class {class_name}" in code:
            raise ValueError(
                f"Class definition for {class_name} found in the pytest tests."
            )

        return code

    def remove_class_definition(self, code: str, class_name: str) -> str:
        # Pattern to match class definition
        class_pattern = rf"""
            \s*class\s+{re.escape(class_name)}\s*(\([^)]*\))?\s*:  # Class definition
            (?:\s*[\"\'][\"\'][\"\'][\s\S]*?[\"\'][\"\'][\"\'])?  # Optional docstring
            (?:\s*(?!def\s+test_)[\s\S])*?  # Class body (non-greedy)
            (?=\n(?:(?!def\s|class\s)\s*\S|$))  # Look ahead for end of class
        """

        # Function to check if a match is within a patch context
        def is_within_patch(match):
            start = match.start()
            preceding_lines = code[:start].split("\n")[
                -3:
            ]  # Check up to 3 lines before
            return any(
                "@patch" in line or "mock.patch" in line or "with patch" in line
                for line in preceding_lines
            )

        # Find all class definitions
        matches = list(re.finditer(class_pattern, code, re.VERBOSE | re.MULTILINE))

        # Remove class definitions that are not within patch contexts
        for match in reversed(matches):  # Reverse to avoid index issues when removing
            if not is_within_patch(match):
                code = code[: match.start()] + code[match.end() :]

        return code

        return code
