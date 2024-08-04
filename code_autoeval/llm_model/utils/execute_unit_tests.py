"""Execute the unit tests for the provided function."""

import os
import subprocess
from pathlib import Path
from typing import Optional

import pandas as pd
from multiuse.model import class_data_model

from code_autoeval.llm_model.utils import (
    extraction,
    model,
    model_response,
    preprocess_code_before_exec,
)


class ExecuteUnitTests(
    preprocess_code_before_exec.PreProcessCodeBeforeExec,
    extraction.ParseUnitTestCoverage,
):
    coverage_result: subprocess.CompletedProcess = None

    def parse_existing_tests_or_raise_exception(
        self,
        function_attributes: model.FunctionAttributes,
        df: pd.DataFrame,
        class_model: Optional[class_data_model.ClassDataModel] = None,
        attempt: int = 0,
        error_message: str = "",
    ) -> model.UnitTestSummary:
        """Parse the existing tests or raise an exception if tests are missing."""
        if (
            function_attributes.test_absolute_file_path
            and function_attributes.module_absolute_path
            and Path(function_attributes.test_absolute_file_path).exists()
            and Path(function_attributes.module_absolute_path).exists()
            and attempt == 0
            and not error_message
        ):
            try:
                unit_test_summary = self.run_tests(
                    function_attributes.test_absolute_file_path,
                    class_model,
                    df,
                )
                return unit_test_summary.return_or_raise()
            except model.MissingCoverageException:
                return model.UnitTestSummary.create_empty()

        print("No tests found or coverage is not 100%. Creating empty UnitTestSummary")

        # raise Exception("No tests found or coverage is not 100%")
        return model.UnitTestSummary.create_empty()

    def write_code_and_tests(
        self,
        code: str,
        pytest_tests: str,
        class_model: class_data_model.ClassDataModel,
        func_attributes: model.FunctionAttributes,
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

        func_attributes.module_generated_absolute_path.unlink(missing_ok=True)
        func_attributes.test_absolute_file_path.unlink(missing_ok=True)

        # Write the main code to a file
        with open(func_attributes.module_generated_absolute_path, "w") as f:
            f.write(code)

        # Write the pytest tests to a separate file
        with open(func_attributes.test_absolute_file_path, "w") as f:
            f.write(pytest_tests)

        print(f"Main code written to {func_attributes.module_generated_absolute_path}")
        print(f"Pytest tests written to {func_attributes.test_absolute_file_path}")

    def run_tests(
        self,
        test_file_path: Path,
        class_model: class_data_model.ClassDataModel,
        df: Optional[pd.DataFrame] = None,
    ) -> model.UnitTestSummary:
        # Create a temporary file to store the dataframe if provided
        df_path = model_response.SerializeDataframes.store_df_in_temp_file(df)

        self._log_code(
            class_model.coverage_file_path, intro_message="code_path_to_cover: "
        )

        try:
            # Prepare the pytest command
            pytest_command = [
                "pytest",
                str(test_file_path.resolve()),
                "-v",
                f"--cov={class_model.coverage_file_path}",
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

            tests_failed = False

            try:
                # Run pytest first time to display output
                subprocess.run(pytest_command[:-1], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running pytest: {e}")
                print(f"Command: {pytest_command}")
                tests_failed = True

            # with contextlib.suppress(subprocess.CalledProcessError):
            #    # Run pytest first time to display output
            #    subprocess.run(pytest_command[:-1], check=True)

            # Run pytest with coverage
            self.coverage_result = subprocess.run(
                pytest_command,
                capture_output=True,
                text=True,
            )

            self._log_coverage_results(self.coverage_result)

            unit_test_summary: model.UnitTestSummary = (
                self.wrap_run_parse_unit_test_cov(
                    self.coverage_result.stdout,
                    project_root=self.common.project_root,
                    relative_path=class_model.coverage_file_path,
                    func_name=self.init_kwargs.func_name.split(".")[-1],
                    tests_failed=tests_failed,
                )
            )

            unit_test_summary.print_summary()

            return unit_test_summary.return_or_raise()

        finally:
            # Clean up the temporary dataframe file if it was created
            if df_path:
                os.unlink(df_path)
