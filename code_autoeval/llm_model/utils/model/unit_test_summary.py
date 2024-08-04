"""Data Models for the Unit Test Summaries."""

from typing import Dict, Tuple

from pydantic import BaseModel, Field, computed_field

from code_autoeval.llm_model.utils.model.custom_exceptions import (
    MissingCoverageException,
)


class UnitTestSummary(BaseModel):

    uncovered_lines: Dict[Tuple[int, int], str] = Field(
        default={},
        description="The lines that were not covered by the unit tests.",
    )

    extracted_coverage: float = Field(
        default=0,
        description="The total coverage of the unit tests.",
    )

    recalculated_coverage: float = Field(
        default=0,
        description="The recalculated coverage of the unit tests.",
    )

    tests_failed: bool = Field(
        default=False,
        description="Flag to indicate if the tests failed.",
    )

    @computed_field
    def is_coverage_missing(self) -> bool:
        """Flag to indicate if the coverage is missing."""
        return self.recalculated_coverage < 100

    @computed_field
    def is_fully_covered(self) -> bool:
        """Flag to indicate if the code is fully covered."""
        return self.recalculated_coverage == 100

    def print_summary(self) -> "UnitTestSummary":
        """Print the summary of the unit tests."""
        print(f"Extracted coverage: {self.extracted_coverage}%")
        print(f"Recalculated coverage: {self.recalculated_coverage}%")
        print(f"Uncovered lines: {self.uncovered_lines}")
        print(f"Is coverage missing: {self.is_coverage_missing}")
        print(f"Is fully covered: {self.is_fully_covered}")

        return self

    @classmethod
    def create_empty(cls) -> "UnitTestSummary":
        """Create an empty UnitTestSummary instance with default values."""
        return cls()

    def return_or_raise(self) -> "UnitTestSummary":
        """Return the instance if the coverage is 100%, otherwise raise an exception."""
        if self.tests_failed:
            raise MissingCoverageException("Tests failed")

        if self.is_fully_covered:
            return self

        raise MissingCoverageException("Tests failed or coverage is not 100%")
