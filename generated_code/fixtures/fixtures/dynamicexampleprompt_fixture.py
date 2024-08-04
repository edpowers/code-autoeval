from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.prompting.dynamic_example_prompt import DynamicExamplePrompt
@pytest.fixture
def fixture_mock_dynamicexampleprompt():
    mock = MagicMock(spec=DynamicExamplePrompt)
    mock.generate_act = MagicMock()
    mock.generate_arrange = MagicMock()
    mock.generate_assert = MagicMock()
    mock.generate_fixture_check = MagicMock()
    mock.generate_init_test = MagicMock()
    mock.generate_mock_return_value = MagicMock()
    mock.provide_test_structure = MagicMock()
    return mock
