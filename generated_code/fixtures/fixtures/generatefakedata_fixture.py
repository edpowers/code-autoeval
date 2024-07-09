from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.generate_fake_data import GenerateFakeData
from pathlib import Path
from typing import Any, Dict
from code_autoeval.llm_model.utils.model_response.stream_response import StreamResponse
from code_autoeval.llm_model.utils.preprocess_code_before_execution import PreProcessCodeBeforeExecution
from code_autoeval.llm_model.utils.system_prompts import SystemPrompts
from generated_code.fixtures.fixtures.streamresponse_fixture import fixture_mock_streamresponse
from generated_code.fixtures.fixtures.preprocesscodebeforeexecution_fixture import fixture_mock_preprocesscodebeforeexecution
from generated_code.fixtures.fixtures.systemprompts_fixture import fixture_mock_systemprompts
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
@pytest.fixture
def fixture_mock_generatefakedata():
    mock = MagicMock(spec=GenerateFakeData)
    mock.coverage_result = None
    mock.file_path = Path()
    mock.test_file_path = Path()
    mock.absolute_path_from_root = Path()
    mock.unique_imports_dict = {}
    mock.async_generate_fake_data = MagicMock()
    mock.generate_fake_data = MagicMock()
    return mock