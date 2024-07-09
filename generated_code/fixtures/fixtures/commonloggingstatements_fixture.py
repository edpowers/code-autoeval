from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.logging_statements.common_logging_statements import CommonLoggingStatements
from pathlib import Path
from typing import Any, Dict
from code_autoeval.llm_model.utils.base_llm_class import BaseLLMClass
from generated_code.fixtures.fixtures.basellmclass_fixture import fixture_mock_basellmclass
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
@pytest.fixture(name="fixture_mock_commonloggingstatements")
def fixture_mock_commonloggingstatements():
    mock = MagicMock(spec=CommonLoggingStatements)
    mock.coverage_result = None
    mock.file_path = Path("/")
    mock.test_file_path = Path("/")
    mock.absolute_path_from_root = Path("/")
    mock.unique_imports_dict = {}
    mock._log_code = MagicMock()
    mock._log_coverage_results = MagicMock()
    mock._log_fake_gen_data = MagicMock()
    mock._log_max_retries = MagicMock()
    mock._log_test_coverage_path = MagicMock()
    return mock
