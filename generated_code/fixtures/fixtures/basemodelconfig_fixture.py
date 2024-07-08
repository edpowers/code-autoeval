from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.base_llm_class import BaseModelConfig
@pytest.fixture
def fixture_mock_basemodelconfig():
    mock = MagicMock(spec=BaseModelConfig)
    return mock