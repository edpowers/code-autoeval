"""Data Models for the Unit Test Summaries."""

from typing import Dict, Tuple

from pydantic import BaseModel, Field, computed_field


class UnitTestSummary(BaseModel):

    uncovered_lines: Dict[Tuple[int, int], str] = Field(
        default=(None, None),
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

    @computed_field
    def is_coverage_missing(self) -> bool:
        """Flag to indicate if the coverage is missing."""
        return len(self.uncovered_lines) > 0

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
