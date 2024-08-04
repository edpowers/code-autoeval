from unittest.mock import MagicMock

## :
## ```python
import pytest
from code_autoeval.llm_model.utils.model.function_attributes import FunctionAttributes
from code_autoeval.llm_model.utils.prompting.system_prompts import SystemPrompts


@pytest.fixture(scope='module')
def mock_systemprompts():
    return SystemPrompts()

def test_generate_system_prompt_no_existing_function(mock_systemprompts):
    # Arrange
    query = "Example query"
    goal = "Example goal"
    function_attributes = FunctionAttributes(func_name="example_function", is_coroutine=False, function_signature="def example_function():", function_docstring="Example docstring")
    
    instance = mock_systemprompts

    # Act
    result = instance.generate_system_prompt_no_existing_function(query, goal, function_attributes)

    # Assert
    assert isinstance(result, str), "The result should be a string"
    assert query in result, "The query should be included in the result"
    assert goal in result, "The goal should be included in the result"
    assert function_attributes.func_name in result, "The function name should be included in the result"
    assert str(function_attributes.is_coroutine) in result, "The coroutine status should be included in the result"
    assert function_attributes.function_signature in result, "The function signature should be included in the result"
    assert function_attributes.function_docstring in result, "The docstring should be included in the result"