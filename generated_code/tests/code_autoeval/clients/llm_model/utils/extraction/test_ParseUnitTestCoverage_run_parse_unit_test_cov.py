import pathlib
import sys
from unittest.mock import MagicMock, patch

import pytest

# Assuming the function is in a module named parse_unit_test_coverage
sys.path.append("/path/to/your/module")  # Adjust this to your actual module path
from code_autoeval.llm_model.utils.extraction.parse_unit_test_coverage import (
    ParseUnitTestCoverage,
)


@pytest.mark.asyncio
async def test_run_parse_unit_test_cov():
    # Arrange
    coverage_output = "some_coverage_output"
    project_root = pathlib.Path("/path/to/project")
    relative_path = "example.py"
    func_name = "example_function"

    instance = ParseUnitTestCoverage()
    mock_parse_result = (None, ["1:2-3:4"])  # Mocking the parse result
    mock_uncovered_lines = {(1, 2): "line content"}
    mock_recalculated_coverage = 90.0

    with patch(
        "code_autoeval.llm_model.utils.extraction.parse_unit_test_coverage.ParseUnitTestCoverage._parse_coverage_output",
        return_value=mock_parse_result,
    ):
        with patch(
            "code_autoeval.llm_model.utils.extraction.parse_unit_test_coverage.ParseUnitTestCoverage._parse_missing_ranges",
            return_value={},
        ):
            with patch(
                "code_autoeval.llm_model.utils.extraction.parse_unit_test_coverage.ParseUnitTestCoverage._find_uncovered_lines",
                return_value=mock_uncovered_lines,
            ):
                with patch(
                    "code_autoeval.llm_model.utils.extraction.parse_unit_test_coverage.ParseUnitTestCoverage._recalculate_coverage",
                    return_value=mock_recalculated_coverage,
                ):
                    # Act
                    result = await instance.run_parse_unit_test_cov(
                        coverage_output, project_root, relative_path, func_name
                    )

                    # Assert
                    assert result == (
                        mock_uncovered_lines,
                        mock_recalculated_coverage,
                    )  # Assert
                    assert result == (mock_uncovered_lines, mock_recalculated_coverage)
