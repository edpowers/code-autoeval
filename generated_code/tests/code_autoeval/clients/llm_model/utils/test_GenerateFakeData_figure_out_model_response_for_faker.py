from unittest.mock import patch

import pytest
from code_autoeval.clients.llm_model.utils.generate_fake_data import GenerateFakeData

# Analysis of the function:
# The function is designed to extract content from a model's response, which can be either a string or a dictionary.
# It checks if the response is a string and returns it directly. If not, it looks for 'response' or 'content' keys in the dictionary.
# If neither key is found, it raises a ValueError with an error message indicating the unexpected format of the response.

def test_normal_use_case():
    # Arrange
    response = "This is a normal string response."
    
    # Act
    result = GenerateFakeData().figure_out_model_response_for_faker(response)
    
    # Assert
    assert result == response, f"Expected {response}, but got {result}"

def test_dict_with_response_key():
    # Arrange
    response = {"response": "This is a dictionary response with 'response' key."}
    
    # Act
    result = GenerateFakeData().figure_out_model_response_for_faker(response)
    
    # Assert
    assert result == response["response"], f"Expected {response['response']}, but got {result}"

def test_dict_with_content_key():
    # Arrange
    response = {"content": "This is a dictionary response with 'content' key."}
    
    # Act
    result = GenerateFakeData().figure_out_model_response_for_faker(response)
    
    # Assert
    assert result == response["content"], f"Expected {response['content']}, but got {result}"

def test_unexpected_format():
    # Arrange
    response = {"unexpected": "This is an unexpected format."}
    
    # Act & Assert
    with pytest.raises(ValueError):
        GenerateFakeData().figure_out_model_response_for_faker(response)

def test_empty_string():
    # Arrange
    response = ""
    
    # Act
    result = GenerateFakeData().figure_out_model_response_for_faker(response)
    
    # Assert
    assert result == response, f"Expected {response}, but got {result}"