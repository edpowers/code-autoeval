from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest
from code_autoeval.clients.llm_model.utils.generate_fake_data import GenerateFakeData

# Analysis of the function provided:
# The function `GenerateFakeData.generate_fake_data` is designed to generate fake data based on a given function's signature.
# It uses an asynchronous method `async_generate_fake_data` which it runs in an event loop for synchronous execution.
# This setup allows the function to handle async code seamlessly within a sync context, making it versatile and efficient.

@patch("code_autoeval.clients.llm_model.utils.generate_fake_data.GenerateFakeData.__init__", return_value=None)
def test_normal_case(mock_init):
    # Arrange
    mock_func = MagicMock()
    expected_df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    
    # Act
    result = GenerateFakeData.generate_fake_data(mock_func, df=expected_df)
    
    # Assert
    assert isinstance(result, pd.DataFrame), "The output should be a DataFrame"
    pd.testing.assert_frame_equal(result, expected_df)

def test_edge_case_no_data():
    # Arrange
    mock_func = MagicMock()
    
    # Act
    result = GenerateFakeData.generate_fake_data(mock_func)
    
    # Assert
    assert isinstance(result, pd.DataFrame), "The output should be a DataFrame"
    assert len(result) == 0, "Output DataFrame should have no rows if no input data is provided"

def test_error_condition():
    # Arrange
    mock_func = MagicMock()
    
    # Act & Assert
    with pytest.raises(TypeError):
        GenerateFakeData.generate_fake_data("not a function")

def test_debug_mode():
    # Arrange
    mock_func = MagicMock()
    expected_df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    
    # Act
    result = GenerateFakeData.generate_fake_data(mock_func, df=expected_df, debug=True)
    
    # Assert
    assert isinstance(result, pd.DataFrame), "The output should be a DataFrame"
    pd.testing.assert_frame_equal(result, expected_df)

def test_skip_generate():
    # Arrange
    mock_func = MagicMock()
    expected_df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    
    # Act
    result = GenerateFakeData.generate_fake_data(mock_func, df=expected_df, skip_generate_fake_data=True)
    
    # Assert
    assert isinstance(result, pd.DataFrame), "The output should be a DataFrame"
    pd.testing.assert_frame_equal(result, expected_df)