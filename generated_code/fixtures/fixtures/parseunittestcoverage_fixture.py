from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.extraction.parse_unit_test_coverage import ParseUnitTestCoverage
from pathlib import Path
from typing import Any, Dict
from code_autoeval.llm_model.utils.logging_statements.logging_statements import LoggingStatements
from generated_code.fixtures.fixtures.loggingstatements_fixture import fixture_mock_loggingstatements
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
@pytest.fixture
def fixture_mock_parseunittestcoverage():
    mock = MagicMock(spec=ParseUnitTestCoverage)
    mock.coverage_result = None
    mock.file_path = Path('/')
    mock.test_file_path = Path('/')
    mock.absolute_path_from_root = Path('/')
    mock.unique_imports_dict = {}
    mock.run_parse_unit_test_cov = None
    return mock