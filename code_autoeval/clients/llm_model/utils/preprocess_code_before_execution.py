"""Class for preprocessing code before execution."""


import os
import re
import subprocess
import tempfile
from typing import Tuple

from code_autoeval.clients.llm_model.utils.file_path_functions import FilePathFunctions


class PreProcessCodeBeforeExecution(FilePathFunctions):

    base_dir: str = "generated_code"

    def preprocess_code(self, code: str, max_line_length: int = 120) -> str:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        try:
            # Run flake8 on the entire file
            flake8_result = subprocess.run(
                ['flake8', '--select=E999,F401,F821,E501', temp_file_path],
                capture_output=True,
                text=True
            )

            # Process the flake8 output
            problematic_lines = set()
            import_errors = []
            for line in flake8_result.stdout.splitlines():
                parts = line.split(':')
                if len(parts) >= 4:
                    line_num = int(parts[1])
                    error_code = parts[3].strip().split()[0]
                    if error_code in ['F401', 'F821']:
                        import_errors.append(line)
                    else:
                        problematic_lines.add(line_num)

            # Raise an error if there are import issues
            if import_errors:
                raise ImportError("Import errors found:\n" + "\n".join(import_errors))

            # Process the code
            lines = code.splitlines()
            processed_lines = []
            for i, line in enumerate(lines, 1):
                if i not in problematic_lines and len(line) <= max_line_length:
                    processed_lines.append(line)

            return '\n'.join(processed_lines)

        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)

    def split_main_and_example(self, code: str) -> Tuple[str, str]:
        parts = code.split('if __name__ == "__main__":')
        if len(parts) == 2:
            return parts[0].strip(), f'if __name__ == "__main__":{parts[1]}'
        return code, ""

    def clean_code(self, code: str) -> str:
        # Remove markdown code blocks if present
        code = re.sub(r"```python\n|```", "", code)
        # Remove leading/trailing whitespace
        return code.strip()

    def ensure_imports(self, pytest_tests: str, func_name: str, debug: bool = False) -> str:
        required_imports = f"import pytest\nimport pandas as pd\nfrom {self.base_dir}.{func_name} import {func_name}\n\n"

        # Check if the imports are already present
        if not pytest_tests.startswith(required_imports):
            # If not, add them at the beginning
            pytest_tests = required_imports + pytest_tests

        # Update the import statement
        # pytest_tests = self.update_import_statement(pytest_tests, func_name, self.base_dir, debug=debug)

        return pytest_tests
