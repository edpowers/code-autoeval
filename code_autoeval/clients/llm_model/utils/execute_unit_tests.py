"""Execute the unit tests for the provided function."""

import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd
from IPython.display import display

from code_autoeval.clients.llm_model.utils.preprocess_code_before_execution import (
    PreProcessCodeBeforeExecution,
)


class CoverageParsingError(Exception):
    pass


class ExecuteUnitTests(PreProcessCodeBeforeExecution):

    coverage_result: subprocess.CompletedProcess = None
    file_path: str = None
    test_file_path: str = None

    def write_code_and_tests(self, code: str, pytest_tests: str, func_name: str) -> None:
        # Preprocess the code and tests
        code = self.preprocess_code(code)
        pytest_tests = self.preprocess_code(pytest_tests)

        # Clean up the code and tests
        code = self.clean_code(code)
        pytest_tests = self.clean_code(pytest_tests)

        # Ensure proper imports in the test file
        pytest_tests = self.ensure_imports(pytest_tests, func_name)

        # Split the main code and the example usage
        # main_code, example_code = self.split_main_and_example(code)
        base_directory = "generated_code"
        self.file_path = f"{base_directory}/{func_name}.py"
        self.test_file_path = f"{base_directory}/tests/test_{func_name}.py"

        # Create the directory if it does not exist
        os.makedirs(Path(self.test_file_path).parent, exist_ok=True, mode=0o777)

        # Write the main code to a file
        with open(self.file_path, "w") as f:
            f.write(code)

        # Write the pytest tests to a separate file
        with open(self.test_file_path, "w") as f:
            f.write(pytest_tests)

        print(f"Main code written to {self.file_path}")
        print(f"Pytest tests written to {self.test_file_path}")


    def run_tests(self, func_name: str, df: Optional[pd.DataFrame] = None) -> bool:
        if self.test_file_path is None:
            raise ValueError("No test file path set. Please write tests first.")

        # func_name = os.path.basename(self.test_file_path)[5:-3]  # Remove 'test_' prefix and '.py' suffix
        print("\nRunning pytest with coverage:")

        # Get the directory containing generated_code
        base_dir = os.path.dirname(os.path.dirname(self.test_file_path))

        # Create a temporary file to store the dataframe if provided
        if df is not None:
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.pkl', delete=False) as temp_df_file:
                df.to_pickle(temp_df_file.name)
                df_path = temp_df_file.name
        else:
            df_path = None

        try:
            # Prepare the pytest command
            pytest_command = [
                "pytest",
                self.test_file_path,
                "-v",
                f"--cov=generated_code.{func_name}",
                "--cov-report=term-missing",
                "--cov-fail-under=100",
            ]

            # Set up the environment with the updated PYTHONPATH
            env = os.environ.copy()
            env["PYTHONPATH"] = f"{base_dir}:{env.get('PYTHONPATH', '')}"

            # Add dataframe path as a command-line option if available
            # TODO: Add in this functionality so that it works with latest pytest.
            # if df_path:
            #     pytest_command.append(f"--df_path={df_path}")

            # Run pytest with coverage
            self.coverage_result = subprocess.run(
                pytest_command,
                capture_output=True,
                text=True,
            )

            # Print the pytest output
            print(self.coverage_result.stdout)
            if self.coverage_result.stderr:
                print("Errors:")
                print(self.coverage_result.stderr)

            try:
                coverage_data = self.parse_coverage(self.coverage_result.stdout, self.file_path)
                target_coverage = coverage_data[self.file_path]
                print(f"Parsed coverage for {func_name}.py: {target_coverage}%")
                if target_coverage < 100:
                    print(f"Warning: Code coverage is not 100%. Actual coverage: {target_coverage}%")
                    return False
                return self.coverage_result.returncode == 0  # Return True if tests passed
            except CoverageParsingError as e:
                print(f"Error parsing coverage: {e}")
                return False

        finally:
            # Clean up the temporary dataframe file if it was created
            if df_path:
                os.unlink(df_path)


    def parse_coverage(self, output: str, target_file: str) -> Dict[str, int]:
        coverage_data = {}

        # Remove ANSI escape codes
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_output = ansi_escape.sub('', output)

        for line in clean_output.split('\n'):

            if "TOTAL" in line:
                parts = line.split()
                # Find the part that contains the coverage percentage
                for part in parts:
                    if part.endswith("%"):
                        try:
                            coverage_percentage = int(part.rstrip('%'))
                            coverage_data[target_file] = coverage_percentage
                        except ValueError as ve:
                            print(f"Error parsing coverage percentage for {target_file}: {ve}")
                            print(f"Line content: {line}")
                        break

        if not coverage_data:
            display(clean_output)
            raise CoverageParsingError("Coverage information not found in the output.")

        if target_file not in coverage_data:
            raise CoverageParsingError(f"Coverage for {target_file} not found in the output.")

        return coverage_data


    def get_coverage_report(self, function_name: str) -> Dict[str, Any]:
        """Get the coverage report for the executed tests."""
        # Initialize default values
        total_coverage = 0
        uncovered_lines = "None"

        # Parse the coverage report
        coverage_output = self.coverage_result.stdout

        # Find the line containing coverage information for our function
        coverage_pattern = rf"{function_name}\.py\s+\d+\s+\d+\s+(\d+)%\s+([\d,-]+)?"
        if match := re.search(coverage_pattern, coverage_output):
            total_coverage = int(match[1])
            uncovered_lines = match[2] or "None"

        # Extract test results summary
        test_summary = re.search(r'(=+ .*? =+)$', coverage_output, re.MULTILINE | re.DOTALL)
        test_summary = (
            test_summary[1] if test_summary else "No test summary available."
        )

        return {
            "total_coverage": total_coverage,
            "uncovered_lines": uncovered_lines,
            "test_summary": test_summary,
            "full_output": coverage_output
        }

    def verify_goal(self, result: Any, goal: str, df: pd.DataFrame) -> bool:
        """
        Verify if the generated code meets the specified goal.

        :param result: The result of executing the generated code
        :param goal: The specified goal for the function
        :param df: The input dataframe
        :return: True if the goal is met, False otherwise
        """
        if goal == "replace every instance of 'Australia'":
            if isinstance(result, pd.DataFrame):
                return not result.applymap(lambda x: 'Australia' in str(x)).any().any()

        # Add more goal verifications as needed

        return False  # Default to False if goal is not recognized


# Add this function to your test file to load the dataframe
# @pytest.fixture(scope="module")
# def input_df(request: pytest.FixtureRequest) -> Optional[pd.DataFrame]:
#    if df_path := request.config.getoption("--df_path"):
#        return pd.read_pickle(df_path)
#    return None

# Add this to your test file to add the command-line option#
# def pytest_addoption(parser) -> None:
#    parser.addoption("--df_path", action="store", default=None, help="Path to the input DataFrame pickle file")