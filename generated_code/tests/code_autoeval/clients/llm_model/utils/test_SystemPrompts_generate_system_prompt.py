from unittest.mock import MagicMock, patch

import pytest

from code_autoeval.llm_model.utils.model.class_data_model import ClassDataModel
from code_autoeval.llm_model.utils.model.function_attributes import \
    FunctionAttributes
from code_autoeval.llm_model.utils.system_prompts import SystemPrompts


# Mocking the dependencies
@patch("code_autoeval.llm_model.utils.system_prompts.SystemPrompts.generate_system_prompt_with_existing_function")
@patch("code_autoeval.llm_model.utils.system_prompts.SystemPrompts.generate_system_prompt_no_existing_function")
def test_generate_system_prompt_normal(mock_gen_no_existing, mock_gen_existing):
    # Arrange
    system_prompts = SystemPrompts()
    query = "test query"
    goal = "test goal"
    function_attributes = FunctionAttributes()
    class_model = ClassDataModel()

    # Act
    result = system_prompts.generate_system_prompt(query, goal, function_attributes, class_model)

    # Assert
    mock_gen_no_existing.assert_not_called()
    mock_gen_existing.assert_not_called()
    assert isinstance(result, str)

def test_generate_system_prompt_with_existing_function():
    # Arrange
    system_prompts = SystemPrompts()
    query = "test query"
    goal = "test goal"
    function_attributes = FunctionAttributes()
    class_model = ClassDataModel()

    @patch("code_autoeval.llm_model.utils.system_prompts.SystemPrompts.generate_system_prompt_with_existing_function", return_value="mocked result")
    def test_inner(mock_gen_existing):
        # Act
        result = system_prompts.generate_system_prompt(query, goal, function_attributes, class_model)

        # Assert
        mock_gen_existing.assert_called_once_with(query, goal, function_attributes, class_model)
        assert result == "mocked result"
    test_inner()

def test_generate_system_prompt_no_existing_function():
    # Arrange
    system_prompts = SystemPrompts()
    query = "test query"
    goal = "test goal"
    function_attributes = FunctionAttributes()

    @patch("code_autoeval.llm_model.utils.system_prompts.SystemPrompts.generate_system_prompt_no_existing_function", return_value="mocked result")
    def test_inner(mock_gen_no_existing):
        # Act
        result = system_prompts.generate_system_prompt(query, goal, function_attributes)

        # Assert
        mock_gen_no_existing.assert_called_once_with(query, goal, function_attributes)
        assert result == "mocked result"
    test_inner()    test_inner()