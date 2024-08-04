from unittest.mock import MagicMock

import pandas
import pandas as pd
import pytest
from code_autoeval.llm_model.utils.prompting.dynamic_example_prompt import DynamicExamplePrompt


@pytest.fixture(scope='module')
def mock_dynamicexampleprompt():
    return DynamicExamplePrompt()

# Test case for normal use cases
def test_generate_sample_data_with_df(mock_dynamicexampleprompt):
    # Arrange
    param_name = "df"
    expected_result = "pd.DataFrame({'A': range(10), 'B': range(10, 20)})"
    
    # Act
    result = mock_dynamicexampleprompt.generate_sample_data(param_name)
    
    # Assert
    assert isinstance(result, str)
    assert result == expected_result

# Test case for edge cases with 'dict' in param_name
def test_generate_sample_data_with_dict(mock_dynamicexampleprompt):
    # Arrange
    param_name = "dict"
    expected_result = "{'A': [1, 2], 'B': [3, 4]}"
    
    # Act
    result = mock_dynamicexampleprompt.generate_sample_data(param_name)
    
    # Assert
    assert isinstance(result, str)
    assert result == expected_result

# Test case for error conditions with unknown param_name
def test_generate_sample_data_with_unknown(mock_dynamicexampleprompt):
    # Arrange
    param_name = "unknown"
    expected_result = "MagicMock()"
    
    # Act
    result = mock_dynamicexampleprompt.generate_sample_data(param_name)
    
    # Assert
    assert isinstance(result, str)
    assert result == expected_result

# Test case to check the type of generated data for 'df' param_name
def test_generate_sample_data_type_for_df(mock_dynamicexampleprompt):
    # Arrange
    param_name = "df"
    
    # Act
    result = mock_dynamicexampleprompt.generate_sample_data(param_name)
    
    # Assert
    assert isinstance(result, str)
    df = eval(result)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ['A', 'B']
    assert len(df) == 10
    assert all(df['A'].values == range(10))
    assert all(df['B'].values == range(10, 20))

# Test case to check the type of generated data for 'dict' param_name
def test_generate_sample_data_type_for_dict(mock_dynamicexampleprompt):
    # Arrange
    param_name = "dict"
    
    # Act
    result = mock_dynamicexampleprompt.generate_sample_data(param_name)
    
    # Assert
    assert isinstance(result, str)
    data_dict = eval(result)
    assert isinstance(data_dict, dict)
    assert list(data_dict.keys()) == ['A', 'B']
    assert all(data_dict['A'] == [1, 2])
    assert all(data_dict['B'] == [3, 4])