"""Execute the unit tests for the provided function."""

import contextlib
import os
import re
import subprocess
import tempfile
from pathlib import Path
from pprint import pprint
from typing import Any, Callable, Dict, Optional, Tuple

import pandas as pd
from IPython.display import display
from multiuse.filepaths.system_utils import SystemUtils
from multiuse.model import class_data_model

from code_autoeval.llm_model.utils.extraction.parse_unit_test_coverage import (
    ParseUnitTestCoverage,
)

from code_autoeval.llm_model.utils.model.custom_exceptions import (
    CoverageParsingError,
    FormattingError,
    MissingCoverageException,
)
from code_autoeval.llm_model.utils.model.function_attributes import FunctionAttributes
from code_autoeval.llm_model.utils.preprocess_code_before_execution import (
    PreProcessCodeBeforeExecution,
)


class ExecuteUnitTests(PreProcessCodeBeforeExecution, ParseUnitTestCoverage):

    coverage_result: subprocess.CompletedProcess = None

    def parse_existing_tests_or_raise_exception(
        self,
        function_attributes: FunctionAttributes,
        df: pd.DataFrame,
        class_model: Optional[class_data_model.ClassDataModel] = None,
        attempt: int = 0,
        error_message: str = "",
    ) -> Tuple[str, pd.DataFrame, Dict[str, Any], str]:
        """Parse the existing tests or raise an exception if tests are missing."""
        if (
            function_attributes.test_absolute_file_path
            and function_attributes.module_absolute_path
            and Path(function_attributes.test_absolute_file_path).exists()
            and Path(function_attributes.module_absolute_path).exists()
            and attempt == 0
            and not error_message
        ):
            if unit_test_coverage_missing := self.run_tests(
                self.init_kwargs.func_name,
                function_attributes.module_absolute_path,
                function_attributes.test_absolute_file_path,
                df,
                class_model=class_model,
            ):
                raise MissingCoverageException("Tests failed or coverage is not 100%")

        return (
            "",
            df,
            {},
            "",
        )

    def write_code_and_tests(
        self,
        code: str,
        pytest_tests: str,
        func: Callable,
        class_model: Optional[class_data_model.ClassDataModel] = None,
        func_attributes: Optional[FunctionAttributes] = None,
    ) -> None:

        self.validate_test_in_pytest_code(pytest_tests)

        if not class_model:
            code = self.run_preprocess_pipeline(
                code,
                code_type="function",
                func_name=self.init_kwargs.func_name,
                class_model=class_model,
            )

        pytest_tests = self.run_preprocess_pipeline(
            pytest_tests,
            code_type="pytest",
            func_name=self.init_kwargs.func_name,
            class_model=class_model,
            func_attributes=func_attributes,
            is_pytest_format=True,
        )

        # If there's no function named test within the pytests_tests,
        # then raise an error.
        self.file_path, self.test_file_path, self.absolute_path_from_root = (
            self._construct_file_path_and_test_path(func, class_model)
        )

        self._log_code(
            str(self.absolute_path_from_root), intro_message="absolute_path_from_root:"
        )

        self.file_path.unlink(missing_ok=True)
        self.test_file_path.unlink(missing_ok=True)

        # Write the main code to a file
        with open(self.file_path, "w") as f:
            f.write(code)

        # Write the pytest tests to a separate file
        with open(self.test_file_path, "w") as f:
            f.write(pytest_tests)

        print(f"Main code written to {self.file_path}")
        print(f"Pytest tests written to {self.test_file_path}")

    def _construct_file_path_and_test_path(
        self, func: Callable, class_model: Optional[class_data_model.ClassDataModel] = None
    ) -> Tuple[Path, Path, Path]:
        # Get the absolute path of the function's module
        module_path = Path(SystemUtils.get_class_file_path(func))
        # Create the relative path from the project root
        relative_path = module_path.relative_to(self.common.project_root)

        func_name = self.init_kwargs.func_name

        # Get the directory containing generated_code
        self.absolute_path_from_root = (
            self.common.generated_base_dir / relative_path.parent / f"{func_name}.py"
        )

        self.file_path = self.common.project_root / self.absolute_path_from_root

        # Construct the test file path
        self.test_file_path = (
            self.common.generated_base_dir
            / "tests"
            / relative_path.parent
            / f"test_{func_name}.py"
        )

        if "." in str(self.test_file_path):
            self.test_file_path = self.test_file_path.with_stem(
                self.test_file_path.stem.replace(".", "_")
            ).with_suffix(".py")

        SystemUtils.make_file_dir(self.file_path)
        SystemUtils.make_file_dir(self.test_file_path)

        return self.file_path, self.test_file_path, self.absolute_path_from_root

    def run_tests(
        self,
        func_name: str,
        file_path: Path,
        test_file_path: Path,
        df: Optional[pd.DataFrame] = None,
        class_model: Optional[class_data_model.ClassDataModel] = None,
    ) -> Dict[str, Any]:
        # Get the absolute path from the project root
        format_test_path = SystemUtils.format_path_for_import(test_file_path)
        # Remove the project root from the path
        format_test_path_repl = (
            str(format_test_path).replace(f"{self.common.project_root}.", "").strip(".")
        ).replace(".__init__", "___init__")

        self._log_test_coverage_path(format_test_path_repl)

        # Create a temporary file to store the dataframe if provided
        if df is not None:
            with tempfile.NamedTemporaryFile(
                mode="wb", suffix=".pkl", delete=False
            ) as temp_df_file:
                df.to_pickle(temp_df_file.name)
                df_path = temp_df_file.name
        else:
            df_path = None

        # File path would be the generated path
        code_path_to_cover = (
            class_model.absolute_path.rsplit(".", maxsplit=1)[0]
            if class_model
            else file_path.parent
        )

        self._log_code(code_path_to_cover, intro_message="code_path_to_cover: ")
        try:
            # Prepare the pytest command
            pytest_command = [
                "pytest",
                str(test_file_path.resolve()),
                "-v",
                f"--cov={code_path_to_cover}",
                "--cov-report=term-missing",
                "--cov-fail-under=100",
            ]

            # Set up the environment with the updated PYTHONPATH
            # env = os.environ.copy()
            # env["PYTHONPATH"] = f"{self.project_root}:{env.get('PYTHONPATH', '')}"

            # Add dataframe path as a command-line option if available
            # TODO: Add in this functionality so that it works with latest pytest.
            # if df_path:
            #     pytest_command.append(f"--df_path={df_path}")

            with contextlib.suppress(subprocess.CalledProcessError):
                # Run pytest first time to display output
                subprocess.run(pytest_command[:-1], check=True)

            # Run pytest with coverage
            self.coverage_result = subprocess.run(
                pytest_command,
                capture_output=True,
                text=True,
            )

            # if "No data was collected" in self.coverage_result.stderr:
            #    raise FormattingError(
            #        "No data collected - meaning nothing was run - Removing."
            #    )

            self._log_coverage_results(self.coverage_result)

            try:
                parsed_unit_test_coverage, recalculated_coverage = (
                    ParseUnitTestCoverage.run_parse_unit_test_cov(
                        self.coverage_result.stdout,
                        project_root=self.common.project_root,
                        relative_path=code_path_to_cover,
                        func_name=self.init_kwargs.func_name.split(".")[-1],
                    )
                )

                self._log_code(
                    f"{parsed_unit_test_coverage}",
                    intro_message="parsed_unit_test_coverage: ",
                )
                return self._extracted_from_run_tests_(
                    func_name, recalculated_coverage, parsed_unit_test_coverage
                )
            except (
                ImportError,
                SyntaxError,
                IndentationError,
                ModuleNotFoundError,
            ) as oe:
                raise FormattingError(
                    "Error in importation, formatting, indentation etc.."
                ) from oe
            except CoverageParsingError as e:
                print(f"Error parsing coverage: {e}")
                # If "no tests ran" then throw an error, else return False
                if "no tests ran" in self.coverage_result.stdout:
                    raise FormattingError(
                        "Error in importation, formatting, indentation etc.."
                    ) from e

                raise Exception(
                    "Tests failed or coverage is not 100% - raising exception"
                ) from e

        finally:
            # Clean up the temporary dataframe file if it was created
            if df_path:
                os.unlink(df_path)

    # TODO Rename this here and in `run_tests`
    def _extracted_from_run_tests_(
        self, func_name, recalculated_coverage, parsed_unit_test_coverage
    ):
        coverage_data = self.parse_coverage(
            self.coverage_result.stdout, str(self.file_path)
        )

        # Find the only key in the coverage data.
        coverage_data_key = list(coverage_data.keys())[0]

        target_coverage = coverage_data[coverage_data_key]

        print(f"Parsed coverage for {func_name}.py: {target_coverage}%")
        print(f"Recalculated coverage: {recalculated_coverage:.2f}%")

        if recalculated_coverage >= 100:
            return {}

        print(
            f"Warning: Code coverage is not 100%. Actual coverage: {target_coverage}%"
        )
        return parsed_unit_test_coverage

    def parse_coverage(self, output: str, target_file: str) -> Dict[str, int]:
        coverage_data = {}

        # Remove ANSI escape codes
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        clean_output = ansi_escape.sub("", output)

        for line in clean_output.split("\n"):

            if "TOTAL" in line:
                parts = line.split()
                # Find the part that contains the coverage percentage
                for part in parts:
                    if part.endswith("%"):
                        try:
                            coverage_percentage = int(part.rstrip("%"))
                            coverage_data[target_file] = coverage_percentage
                        except ValueError as ve:
                            print(
                                f"Error parsing coverage percentage for {target_file}: {ve}"
                            )
                            print(f"Line content: {line}")
                        break

        if not coverage_data:
            display(pprint(output))  # type: ignore
            raise CoverageParsingError("Coverage information not found in the output.")

        if target_file not in coverage_data:
            raise CoverageParsingError(
                f"Coverage for {target_file} not found in the output."
            )

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
        test_summary = re.search(
            r"(=+ .*? =+)$", coverage_output, re.MULTILINE | re.DOTALL
        )
        test_summary = test_summary[1] if test_summary else "No test summary available."

        return {
            "total_coverage": total_coverage,
            "uncovered_lines": uncovered_lines,
            "test_summary": test_summary,
            "full_output": coverage_output,
        }
