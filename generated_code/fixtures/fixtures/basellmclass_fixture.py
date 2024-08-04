from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.base_llm_class import BaseLLMClass
from pathlib import Path
from typing import Any, Dict, Optional
from code_autoeval.llm_model.utils.base_llm_class import BaseModelConfig
from generated_code.fixtures.fixtures.basemodelconfig_fixture import fixture_mock_basemodelconfig
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
@pytest.fixture
def fixture_mock_basellmclass():
    mock = MagicMock(spec=BaseLLMClass)
    mock.coverage_result = None
    mock.file_path = Path()
    mock.test_file_path = Path()
    mock.absolute_path_from_root = Path()
    mock.unique_imports_dict = {}
    return mock