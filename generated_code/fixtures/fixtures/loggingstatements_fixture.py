from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.logging_statements.logging_statements import LoggingStatements
from pathlib import Path
from typing import Any, Dict
from code_autoeval.llm_model.utils.logging_statements.common_logging_statements import CommonLoggingStatements
from generated_code.fixtures.fixtures.commonloggingstatements_fixture import fixture_mock_commonloggingstatements
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
@pytest.fixture(name="fixture_mock_loggingstatements")
def fixture_mock_loggingstatements():
    mock = MagicMock(spec=LoggingStatements)
    mock.coverage_result = None
    mock.file_path = Path()
    mock.test_file_path = Path()
    mock.absolute_path_from_root = Path()
    mock.unique_imports_dict = {}
    return mock
