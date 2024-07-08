from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.base_llm_class import LLMModelAttributes
@pytest.fixture
def fixture_mock_llmmodelattributes():
    mock = MagicMock(spec=LLMModelAttributes)
    mock.llm_model_name = ''
    mock.llm_model_url = ''
    return mock