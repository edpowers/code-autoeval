"""Common logging statements."""

import subprocess
from pathlib import Path
from pprint import pprint
from typing import Any, Union

from IPython.display import display

from code_autoeval.llm_model.utils.base_llm_class import BaseLLMClass


class CommonLoggingStatements(BaseLLMClass):

    def _log_max_retries(self, max_retries: int) -> None:
        """Log the max retries."""
        # If we've exhausted all retries
        if self.init_kwargs.verbose:
            self.common.class_logger.debug(
                f"Failed to generate correct code with 100% coverage after {max_retries} attempts."
            )

    def _log_coverage_results(
        self, coverage_result: subprocess.CompletedProcess
    ) -> None:
        """Log the coverage results."""
        # Print the pytest output
        if self.init_kwargs.debug:
            display(pprint(coverage_result))

            self.common.class_logger.debug(
                f"Coverage results: {coverage_result.stdout}"
            )

            if coverage_result.stderr:
                self.common.class_logger.debug(
                    f"Coverage errors: {coverage_result.stderr}"
                )
                display(pprint(coverage_result.stderr))

    def _log_test_coverage_path(self, test_coverage_path: Union[str, Path]) -> None:
        """Log the test coverage path."""
        if self.init_kwargs.debug:
            self.common.class_logger.debug(f"Test coverage path: {test_coverage_path}")

    def _log_fake_gen_data(self, fake_data: Any) -> None:
        """Log the fake gen data path."""
        if self.init_kwargs.debug:
            self.common.class_logger.debug(f"Generated fake DataFrame: {fake_data}")

    def _log_code(self, code: str, intro_message: str = "Generated Code") -> None:
        """Log the generated code."""
        if self.init_kwargs.debug:
            self.common.class_logger.debug(f"{intro_message}\n{code}")
