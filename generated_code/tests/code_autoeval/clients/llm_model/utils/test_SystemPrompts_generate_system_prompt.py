from unittest.mock import MagicMock, patch

import pytest
from code_autoeval.clients.llm_model.utils.model.class_data_model import ClassDataModel
from code_autoeval.clients.llm_model.utils.model.function_attributes import FunctionAttributes
from code_autoeval.clients.llm_model.utils.system_prompts.SystemPrompts import SystemPrompts

# Analysis:
# The function `generate_system_prompt` is designed to generate a system prompt based on the provided query, goal, and function attributes. 
# It has two main behaviors depending on whether there are existing functions or not. If class_model is provided along with function_attributes, 
# it uses `generate_system_prompt_with_existing_function`. Otherwise, it falls back to `generate_system_prompt_no_existing_function`.

def test_normal_use_case():
    # Arrange
    query = "test query"
    goal = "test goal"
    function_attributes = FunctionAttributes()
    class_model = ClassDataModel()
    system_prompts = SystemPrompts()
    
    @patch("code_autoeval.clients.llm_model.utils.system_prompts.SystemPrompts.generate_system_prompt_no_existing_function")
    def mock_generate_system_prompt_no_existing_function(query, goal, function_attributes):
        return "Generated prompt without existing function"
    
    @patch("code_autoeval.clients.llm_model.utils.system_prompts.SystemPrompts.generate_system_prompt_with_existing_function")
    def mock_generate_system_prompt_with_existing_function(query, goal, function_attributes, class_model):
        return "Generated prompt with existing function"
    
    # Act
    result = system_prompts.generate_system_prompt(query, goal, function_attributes)
    
    # Assert
    assert result == "Generated prompt without existing function"

def test_with_existing_function():
    # Arrange
    query = "test query"
    goal = "test goal"
    function_attributes = FunctionAttributes()
    class_model = ClassDataModel()
    system_prompts = SystemPrompts()
    
    @patch("code_autoeval.clients.llm_model.utils.system_prompts.SystemPrompts.generate_system_prompt_with_existing_function")
    def mock_generate_system_prompt_with_existing_function(query, goal, function_attributes, class_model):
        return "Generated prompt with existing function"
    
    # Act
    result = system_prompts.generate_system_prompt(query, goal, function_attributes, class_model)
    
    # Assert
    assert result == "Generated prompt with existing function"

def test_no_existing_function():
    # Arrange
    query = "test query"
    goal = "test goal"
    function_attributes = FunctionAttributes()
    system_prompts = SystemPrompts()
    
    @patch("code_autoeval.clients.llm_model.utils.system_prompts.SystemPrompts.generate_system_prompt_no_existing_function")
    def mock_generate_system_prompt_no_existing_function(query, goal, function_attributes):
        return "Generated prompt without existing function"
    
    # Act
    result = system_prompts.generate_system_prompt(query, goal, function_attributes)
    
    # Assert
    assert result == "Generated prompt without existing function"

def test_edge_case_no_goal():
    # Arrange
    query = "test query"
    goal = ""
    function_attributes = FunctionAttributes()
    system_prompts = SystemPrompts()
    
    @patch("code_autoeval.clients.llm_model.utils.system_prompts.SystemPrompts.generate_system_prompt_no_existing_function")
    def mock_generate_system_prompt_no_existing_function(query, goal, function_attributes):
        return "Generated prompt without existing function"
    
    # Act
    result = system_prompts.generate_system_prompt(query, goal, function_attributes)
    
    # Assert
    assert result == "Generated prompt without existing function"

def test_error_condition():
    # Arrange
    query = None
    goal = "test goal"
    function_attributes = FunctionAttributes()
    system_prompts = SystemPrompts()
    
    @patch("code_autoeval.clients.llm_model.utils.system_prompts.SystemPrompts.generate_system_prompt_no_existing_function")
    def mock_generate_system_prompt_no_existing_function(query, goal, function_attributes):
        return "Generated prompt without existing function"
    
    # Act & Assert
    with pytest.raises(TypeError):
        system_prompts.generate_system_prompt(query, goal, function_attributes)