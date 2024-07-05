from unittest.mock import MagicMock, patch

import pytest
from code_autoeval.clients.llm_model.utils.model.class_data_model import ClassDataModel
from code_autoeval.clients.llm_model.utils.model.function_attributes import FunctionAttributes
from code_autoeval.clients.llm_model.utils.system_prompts import SystemPrompts


# Mocking the required classes and methods for testing
@patch("code_autoeval.clients.llm_model.utils.system_prompts.SystemPrompts.__init__", return_value=None)
def test_generate_system_prompt_with_existing_function(mock_init):
    # Arrange
    query = "Implement the method."
    goal = "Refactor code to handle edge cases and improve efficiency."
    function_attributes = FunctionAttributes(
        func_name="generate_system_prompt_with_existing_function",
        is_coroutine=False,
        function_signature="(self, query: str, goal: str, function_attributes: FunctionAttributes, class_model: ClassDataModel) -> str",
        function_docstring="""Function Body:""",
        function_body="""return f\"\"\"{query} - with {goal}\"\"\""""
    )
    class_model = ClassDataModel(
        absolute_path="code_autoeval.clients.llm_model.utils.system_prompts.SystemPrompts",
        base_classes=["object"],
        init_params=[],
        class_attributes=[]
    )
    
    system_prompts = SystemPrompts()
    
    # Act
    result = system_prompts.generate_system_prompt_with_existing_function(query, goal, function_attributes, class_model)
    
    # Assert
    assert result == f"{query} - with {goal}"