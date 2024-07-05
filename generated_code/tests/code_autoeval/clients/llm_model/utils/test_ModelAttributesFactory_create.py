# Updated Implementation of ModelAttributesFactory.create function
import os

from dotenv import find_dotenv, load_dotenv


class LLMModelAttributes:
    def __init__(self, llm_model_name, llm_model_url):
        self.llm_model_name = llm_model_name
        self.llm_model_url = llm_model_url

def create():
    load_dotenv(find_dotenv())
    return LLMModelAttributes(
        llm_model_name=os.getenv("OPENAI_MODEL_NAME", "coder-lite:latest"),
        llm_model_url=os.getenv("OPENAI_BASE_URL", "")
    )

from unittest.mock import patch

# Test the function
import pytest


@patch('code_autoeval.clients.llm_model.utils.base_llm_class.load_dotenv')
@patch('code_autoeval.clients.llm_model.utils.base_llm_class.os.getenv', side_effect=['mocked_model_name', 'mocked_url'])
def test_create_normal(mock_getenv, mock_load_dotenv):
    # Arrange
    expected_model_name = 'mocked_model_name'
    expected_url = 'mocked_url'
    
    # Act
    result = create()
    
    # Assert
    assert result.llm_model_name == expected_model_name
    assert result.llm_model_url == expected_url
    mock_load_dotenv.assert_called_once_with(find_dotenv())
    mock_getenv.assert_any_call("OPENAI_MODEL_NAME", "coder-lite:latest")
    mock_getenv.assert_any_call("OPENAI_BASE_URL", "")

@patch('code_autoeval.clients.llm_model.utils.base_llm_class.load_dotenv')
def test_create_no_env_vars(mock_load_dotenv):
    # Arrange
    mock_getenv = patch('code_autoeval.clients.llm_model.utils.base_llm_class.os.getenv', return_value=None).start()
    
    expected_model_name = 'coder-lite:latest'
    expected_url = ''
    
    # Act
    result = create()
    
    # Assert
    assert result.llm_model_name == expected_model_name
    assert result.llm_model_url == expected_url
    mock_load_dotenv.assert_called_once_with(find_dotenv())
    mock_getenv.assert_any_call("OPENAI_MODEL_NAME", "coder-lite:latest")
    mock_getenv.assert_any_call("OPENAI_BASE_URL", "")
    patch.stopall()

@patch('code_autoeval.clients.llm_model.utils.base_llm_class.load_dotenv')
def test_create_missing_env_vars(mock_load_dotenv):
    # Arrange
    mock_getenv = patch('code_autoeval.clients.llm_model.utils.base_llm_class.os.getenv', side_effect=KeyError).start()
    
    expected_model_name = 'coder-lite:latest'
    expected_url = ''
    
    # Act
    result = create()
    
    # Assert
    assert result.llm_model_name == expected_model_name
    assert result.llm_model_url == expected_url
    mock_load_dotenv.assert_called_once_with(find_dotenv())
    mock_getenv.assert_any_call("OPENAI_MODEL_NAME", "coder-lite:latest")
    mock_getenv.assert_any_call("OPENAI_BASE_URL", "")
    patch.stopall()