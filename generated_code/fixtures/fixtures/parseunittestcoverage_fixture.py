from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.extraction.parse_unit_test_coverage import ParseUnitTestCoverage
from pathlib import Path
from typing import Any, Dict, Optional
from code_autoeval.llm_model.utils.log_funcs.logging_funcs import LoggingFuncs
from generated_code.fixtures.fixtures.loggingfuncs_fixture import fixture_mock_loggingfuncs
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
@pytest.fixture(name="fixture_mock_parseunittestcoverage")
def fixture_mock_parseunittestcoverage():
    mock = MagicMock(spec=ParseUnitTestCoverage)
    mock.coverage_result = None
    mock.file_path = Path()
    mock.test_file_path = Path()
    mock.absolute_path_from_root = Path()
    mock.unique_imports_dict = {}
    mock._find_function_bounds = MagicMock()
    mock._find_uncovered_lines = MagicMock()
    mock._parse_coverage_output = MagicMock()
    mock._parse_coverage_v1 = MagicMock()
    mock._parse_missing_ranges = MagicMock()
    mock._recalculate_coverage = MagicMock()
    mock.get_coverage_report = MagicMock()
    mock.run_parse_unit_test_cov = classmethod(MagicMock())
    setattr(mock, 'run_parse_unit_test_cov', classmethod(getattr(mock, 'run_parse_unit_test_cov').__func__))
    mock.wrap_run_parse_unit_test_cov = staticmethod(MagicMock())
    return mock
