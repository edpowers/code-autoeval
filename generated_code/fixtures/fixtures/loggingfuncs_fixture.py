from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.log_funcs.logging_funcs import LoggingFuncs
from pathlib import Path
from typing import Any, Dict
from code_autoeval.llm_model.utils.log_funcs.common_logging_statements import CommonLoggingStatements
from generated_code.fixtures.fixtures.commonloggingstatements_fixture import fixture_mock_commonloggingstatements
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
@pytest.fixture
def fixture_mock_loggingfuncs():
    mock = MagicMock(spec=LoggingFuncs)
    mock.coverage_result = None
    mock.file_path = Path("/")
    mock.test_file_path = Path("/")
    mock.absolute_path_from_root = Path("/")
    mock.unique_imports_dict = {}
    return mock
