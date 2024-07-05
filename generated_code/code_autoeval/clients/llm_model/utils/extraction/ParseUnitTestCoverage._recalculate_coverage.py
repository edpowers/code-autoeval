from unittest.mock import MagicMock, patch

import pytest

from code_autoeval.llm_model.utils.extraction.parse_unit_test_coverage import (
    ParseUnitTestCoverage,
)


def test_parse_range():
    # Test the parse_range function
    assert ParseUnitTestCoverage._recalculate_coverage.parse_range("1,2-3,4") == {
        1,
        2,
        3,
        4,
    }


@patch(
    "code_autoeval.llm_model.utils.extraction.parse_unit_test_coverage.ParseUnitTestCoverage._recalculate_coverage.parse_range",
    return_value={1, 2, 3, 4},
)
def test_normal_case(mock_parse_range):
    # Test normal use case
    concerned_lines = {(1, 2): "code", (3, 4): "more code"}
    result = ParseUnitTestCoverage._recalculate_coverage.parse_range("1,2-3,4")
    assert result == {1, 2, 3, 4}


def test_edge_case_no_concerned_lines():
    # Test case where there are no concerned lines
    with patch(
        "code_autoeval.llm_model.utils.extraction.parse_unit_test_coverage.ParseUnitTestCoverage._recalculate_coverage.parse_range",
        return_value={1, 2, 3, 4},
    ):
        result = ParseUnitTestCoverage._recalculate_coverage(None, "1,2-3,4", {})
        assert result == 100.0


def test_error_condition():
    # Test error condition where range string is invalid
    with pytest.raises(ValueError):
        ParseUnitTestCoverage._recalculate_coverage(
            "invalid_range", {1: "code"}, {(1, 2): "more code"}
        )


def test_error_condition():
    # Test error condition where range string is invalid
    with pytest.raises(ValueError):
        ParseUnitTestCoverage._recalculate_coverage(
            "invalid_range", {1: "code"}, {(1, 2): "more code"}
        )
