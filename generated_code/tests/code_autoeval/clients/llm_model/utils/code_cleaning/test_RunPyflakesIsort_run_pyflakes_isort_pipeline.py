import subprocess
from pathlib import Path
from typing import Optional, Tuple

from code_autoeval.llm_model.utils.model.class_data_model import ClassDataModel

# Updated Implementation of RunPyflakesIsort.run_pyflakes_isort_pipeline Function


class RunPyflakesIsort:
    def __init__(self):
        pass

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
        if class_model:
            code, import_added = self.add_class_import(code, class_model)
            was_modified = was_modified or import_added

            self._log_code(code, "Code after adding class import: ")
        else:
            self._log_code(
                "No valid class model passed", "Skipping adding class import:"
            )

        # Enforce max line length (commented out as per instructions)
        # lines = code.splitlines()
        # processed_lines = [line for line in lines if len(line) <= max_line_length]

        Path("temp_file.py").unlink()  # Remove temporary file

        return code, was_modified

    def parse_pyflakes_output(self, output: str) -> list:
        unused_imports = []
        for line in output.splitlines():
            if "unused name" in line:
                parts = line.split()
                if len(parts) > 2 and parts[1] == "'":
                    unused_imports.append(parts[-1][:-1])
        return unused_imports

    def remove_unused_imports(self, code: str, imports: list) -> str:
        for imp in imports:
            code = code.replace(f"import {imp}\n", "")
            code = code.replace(f"from {imp} import ", "")
        return code

    def add_class_import(
        self, code: str, class_model: "ClassDataModel"
    ) -> Tuple[str, bool]:
        # This method is not implemented in the provided function body
        pass

    def _log_code(self, code: str, message: str):
        print(message)
        print("-" * 40)
        print(code)
        print("\n" + "-" * 40)


import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_subprocess_run():
    with patch("subprocess.run") as mock_run:
        yield mock_run


@pytest.fixture(autouse=True)
def mock_pathlib_Path():
    with patch("pathlib.Path") as mock_path:
        yield mock_path


class TestRunPyflakesIsort:
    @pytest.mark.parametrize(
        "code, max_line_length, expected_output",
        [
            ("import os\nprint('Hello')", 80, "import os\nprint('Hello')"),
            ("import sys\n# unused import\nprint('Hello')", 80, "print('Hello')"),
        ],
    )
    def test_normal_case(self, code, max_line_length, expected_output):
        runpyflakesisort = RunPyflakesIsort()
        result = runpyflakesisort.run_pyflakes_isort_pipeline(code, max_line_length)
        assert result[0] == expected_output
        assert (
            result[1] is True
        )  # Assuming modifications are made if there are changes in the code

    def test_edge_case_no_modifications(self):
        runpyflakesisort = RunPyflakesIsort()
        code = "import os\nprint('Hello')"
        result = runpyflakesisort.run_pyflakes_isort_pipeline(code, 80)
        assert result[0] == code
        assert result[1] is False

    def test_error_condition_invalid_code(self):
        runpyflakesisort = RunPyflakesIsort()
        with pytest.raises(Exception):
            runpyflakesisort.run_pyflakes_isort_pipeline("invalid code", 80)

    @patch("subprocess.run")
    def test_mocked_isort_output(self, mock_isort):
        mock_isort.return_value = subprocess.CompletedProcess(
            args=["isort"], returncode=0, stdout="sorted code", stderr=""
        )
        runpyflakesisort = RunPyflakesIsort()
        result = runpyflakesisort.run_pyflakes_isort_pipeline(
            "import os\nprint('Hello')", 80
        )
        assert result[0] == "sorted code"
        assert result[1] is True

    @patch("subprocess.run")
    def test_mocked_pyflakes_output(self, mock_pyflakes):
        mock_pyflakes.return_value = subprocess.CompletedProcess(
            args=["pyflakes", "temp_file.py"],
            returncode=0,
            stdout="unused import1\nunused import2",
        )
        runpyflakesisort = RunPyflakesIsort()
        code = "import os\nimport sys\nprint('Hello')"
        result = runpyflakesisort.run_pyflakes_isort_pipeline(code, 80)
        assert "import sys" not in result[0]
        assert result[1] is True
