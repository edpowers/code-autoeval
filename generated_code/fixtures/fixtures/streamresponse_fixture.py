from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.model_response.stream_response import StreamResponse
from pathlib import Path
from typing import Any, Dict
from code_autoeval.llm_model.utils.base_llm_class import BaseLLMClass
from generated_code.fixtures.fixtures.basellmclass_fixture import fixture_mock_basellmclass
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
@pytest.fixture(name="fixture_mock_streamresponse")
def fixture_mock_streamresponse():
    mock = MagicMock(spec=StreamResponse)
    mock.coverage_result = None
    mock.file_path = Path("/")
    mock.test_file_path = Path("/")
    mock.absolute_path_from_root = Path("/")
    mock.unique_imports_dict = {}
    mock.ask_backend_model = MagicMock()
    mock.figure_out_model_response = MagicMock()
    mock.split_content_from_model = MagicMock()
    mock.stream_response = MagicMock()
    return mock
