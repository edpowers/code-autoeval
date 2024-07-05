import re
import subprocess
from pathlib import Path
from typing import Optional, Tuple

from code_autoeval.llm_model.utils.logging_statements.logging_statements import (
    LoggingStatements,
)


class RunPyflakesIsort(LoggingStatements):

    def run_pyflakes_isort_pipeline(
        self,
        code: str,
        max_line_length: int,
        class_model: Optional["ClassDataModel"] = None,
    ) -> Tuple[str, bool]:
        was_modified = False

        # Use isort to sort and clean up imports
        isort_result = subprocess.run(
            ["isort", "-", "--profile", "black", f"--line-length={max_line_length}"],
            input=code,
            capture_output=True,
            text=True,
        )
        if isort_result.returncode == 0:
            code = isort_result.stdout
            was_modified = code != isort_result.stdout

        # Use pyflakes to detect unused imports
        with Path("temp_file.py").open("w") as f:
            f.write(code)

        pyflakes_result = subprocess.run(
            ["pyflakes", "temp_file.py"], capture_output=True, text=True
        )

        if pyflakes_result.returncode == 0:
            unused_imports = self.parse_pyflakes_output(pyflakes_result.stdout)

            self._log_code(f"{unused_imports}", "Unused imports: ")

            if unused_imports:
                code = self.remove_unused_imports(code, unused_imports)
                was_modified = True

        # Add necessary imports if class_model is provided
        # if class_model:
        #    code, import_added = self.add_class_import(code, class_model)
        #    was_modified = was_modified or import_added
        #
        #    self._log_code(code, "Code after adding class import: ")
        # else:
        #    self._log_code(
        #        "No valid class model passed", "Skipping adding class import:"
        #    )

        # Enforce max line length
        # lines = code.splitlines()
        # processed_lines = [line for line in lines if len(line) <= max_line_length]

        # if len(processed_lines) != len(lines):
        #    was_modified = True

        Path("temp_file.py").unlink()  # Remove temporary file

        return code, was_modified

    def parse_pyflakes_output(self, output: str) -> list:
        unused_imports = []
        for line in output.splitlines():
            if "imported but unused" in line:
                parts = line.split("'")
                if len(parts) >= 2:
                    unused_imports.append(parts[1])
        return unused_imports

    def remove_unused_imports(self, code: str, unused_imports: list) -> str:
        lines = code.splitlines()
        new_lines = []
        for line in lines:
            if not any(f"import {imp}" in line for imp in unused_imports):
                new_lines.append(line)
        return "\n".join(new_lines)

    def add_class_import(
        self, code: str, class_model: "ClassDataModel"
    ) -> Tuple[str, bool]:
        """Add import for the class if it's not."""
        absolute_path = class_model.absolute_path.rsplit(".", maxsplit=1)[0]
        new_import_line = f"from {absolute_path} import {class_model.class_name}\n"

        # Remove existing import of the class
        lines = code.splitlines()
        new_lines = []
        was_modified = False
        for line in lines:
            if re.search(rf"\bimport\s+{class_model.class_name}\b", line) or re.search(
                rf"\bfrom\s+.*\s+import\s+.*\b{class_model.class_name}\b", line
            ):
                was_modified = True
                continue
            new_lines.append(line)

        # Add new import if it's not already there
        if new_import_line.strip() not in new_lines:
            import_index = next(
                (
                    i
                    for i, line in enumerate(new_lines)
                    if line.startswith("import") or line.startswith("from")
                ),
                0,
            )
            new_lines.insert(import_index, new_import_line.strip())
            was_modified = True

        return "\n".join(new_lines), was_modified
