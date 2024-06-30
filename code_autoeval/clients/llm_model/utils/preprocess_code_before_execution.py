"""Class for preprocessing code before execution."""

import os
import re
import subprocess
import tempfile
from typing import List, Optional, Tuple

import black

from code_autoeval.clients.llm_model.utils.file_path_functions import FilePathFunctions
from code_autoeval.clients.llm_model.utils.model.class_data_model import ClassDataModel
from code_autoeval.clients.llm_model.utils.run_pyflakes_isort import RunPyflakesIsort
from code_autoeval.clients.llm_model.utils.validation.validate_regexes import (
    ValidateRegexes,
    validate_code,
)


class PreProcessCodeBeforeExecution(
    FilePathFunctions, ValidateRegexes, RunPyflakesIsort
):

    @validate_code()
    def run_preprocess_pipeline(
        self,
        code: str,
        max_line_length: int = 120,
        class_model: Optional[ClassDataModel] = None,
        **kwargs,
    ) -> str:
        code = self.remove_non_code_patterns(code)
        code, was_modified = self.preprocess_code(
            code, max_line_length=max_line_length, class_model=class_model, **kwargs
        )

        if was_modified:
            code, was_modified = self.preprocess_code(
                code, max_line_length=max_line_length, class_model=class_model, **kwargs
            )
        if was_modified:
            raise ValueError("Code was modified twice during preprocessing")

        code = self.format_code_with_black(code, **kwargs)

        self._log_code(code, "Code before pyflakes + isort: ")

        code, was_modified = self.run_pyflakes_isort_pipeline(
            code, max_line_length=max_line_length, class_model=class_model, **kwargs
        )

        return code

    @validate_code()
    def preprocess_code(
        self,
        code: str,
        max_line_length: int = 120,
        class_model: Optional[ClassDataModel] = None,
        **kwargs,
    ) -> Tuple[str, bool]:
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
    ) -> Tuple[str, bool]:
        was_modified = False
        # Run flake8 on the entire file
        flake8_result = subprocess.run(
            ["flake8", "--select=E999,F401,F821,F822,F823,F841,E501", temp_file_path],
            capture_output=True,
            text=True,
        )

        # Process the flake8 output
        problematic_lines, import_errors, undefined_names = self.parse_flake8_output(
            flake8_result
        )

        # Remove duplicate import errors
        import_lines_to_add = []
        # If the import error is related to the class that was supposed to be
        # imported, then use the class_model path to import the class
        for i, error in enumerate(import_errors):
            if class_model and class_model.class_name in error:

                absolute_path = class_model.absolute_path.rsplit(".", maxsplit=1)[0]
                # Then add the absolute import line to the code.
                import_line_to_add = (
                    f"from {absolute_path} import {class_model.class_name}"
                )
                import_lines_to_add.append(import_line_to_add)
                # And then remove the error from the list
                import_errors.pop(i)

        # Raise an error if there are import issues
        if import_errors:
            raise ImportError("Import errors found:\n" + "\n".join(import_errors))

        # Process the code
        lines = code.splitlines()
        processed_lines = [
            line
            for i, line in enumerate(lines, 1)
            if i not in problematic_lines and len(line) <= max_line_length
        ]

        if import_lines_to_add:
            processed_lines = import_lines_to_add + processed_lines
            was_modified = True

        return "\n".join(processed_lines), was_modified

    def parse_flake8_output(
        self, flake8_output: subprocess.CompletedProcess[str]
    ) -> Tuple[set, list, set]:
        # Process the flake8 output
        problematic_lines = set()
        import_errors = []
        undefined_names = set()

        for line in flake8_output.stdout.splitlines():
            parts = line.split(":")
            if len(parts) >= 4:
                line_num = int(parts[1])
                error_code = parts[3].strip().split()[0]
                if error_code in ["F401", "F821"]:
                    undefined_name = (
                        line.split("undefined name")[1].strip().strip("'").strip('"')
                    )

                    if undefined_name in undefined_names:
                        continue

                    undefined_names.add(undefined_name)

                    if len(undefined_name) > 2:
                        import_errors.append(line)
                    else:
                        problematic_lines.add(line_num)
                else:
                    problematic_lines.add(line_num)

        return problematic_lines, import_errors, undefined_names

    def split_main_and_example(self, code: str) -> Tuple[str, str]:
        parts = code.split('if __name__ == "__main__":')
        if len(parts) == 2:
            return parts[0].strip(), f'if __name__ == "__main__":{parts[1]}'
        return code, ""

    @validate_code()
    def remove_non_code_patterns(self, code: str, **kwargs) -> str:
        # Remove markdown code blocks if present
        code = re.sub(r"```python\n|```$|,$", "", code)
        # Remove leading/trailing whitespace
        return code.strip()

    @validate_code()
    def format_code_with_black(self, code: str, **kwargs) -> str:
        """Format the code using Black, removing lines with triple backticks if necessary."""
        lines = code.split("\n")
        cleaned_lines = self._remove_problematic_lines(lines)

        try:
            formatted_code = black.format_str(
                "\n".join(cleaned_lines), mode=black.FileMode()
            )
            return formatted_code
        except black.InvalidInput as e:
            # If Black still can't format the code, return the cleaned but unformatted code
            print(f"Warning: Black couldn't format the code. Error: {e}")
            return code

    def _remove_problematic_lines(self, lines: List[str]) -> List[str]:
        """Remove lines containing triple backticks."""
        return [line for line in lines if "`" not in line]

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
                        # If we can't identify the specific line, remove the last line
                        lines.pop()
                else:
                    # If we can't parse the error message, remove the last line
                    lines.pop()

        # If we've removed all lines, return an empty string
        if not lines:
            raise ValueError("All lines were removed during formatting")

        return black.format_str("\n".join(lines), mode=black.FileMode())
