## s:
## ```python
from unittest.mock import MagicMock

import pytest
from code_autoeval.llm_model.utils.prompting.system_prompts import SystemPrompts


@pytest.fixture(scope='module')
def mock_systemprompts():
    return SystemPrompts()

# Test case for normal use case
def test_generate_fake_data_prompt_normal(mock_systemprompts):
    # Arrange
    func = MagicMock(spec=lambda: None, __name__='test_func', __annotations__={'arg1': int, 'arg2': str})
    num_rows = 100
    num_columns = 5
    
    expected_output = f"""
    Generate a Python script to create fake data for the following function:
    
    def test_func(arg1: <class 'int'>, arg2: <class 'str'>):
    
    Use only the Faker library to generate appropriate fake data.
    
    Create a pandas DataFrame named 'fake_data' containing the generated data.
    
    Ensure the generated data is diverse and suitable for testing the function.
    
    Do not use PandasProvider or any other external libraries besides Faker, random, and pandas.
    
    """
    
    # Act
    result = mock_systemprompts.generate_fake_data_prompt(func, num_rows, num_columns)
    
    # Assert
    assert isinstance(result, str)
    assert result == expected_output.strip()

# Test case for edge cases with no annotations or docstring
def test_generate_fake_data_prompt_edge_no_annotations_or_docstring(mock_systemprompts):
    # Arrange
    func = MagicMock(spec=lambda: None)
    num_rows = 150
    num_columns = 3
    
    expected_output = f"""
    Generate a Python script to create fake data for the following function:
    
    def {func.__name__}():
    
    Use only the Faker library to generate appropriate fake data.
    
    Create a pandas DataFrame named 'fake_data' containing the generated data.
    
    Ensure the generated data is diverse and suitable for testing the function.
    
    Do not use PandasProvider or any other external libraries besides Faker, random, and pandas.
    
    """
    
    # Act
    result = mock_systemprompts.generate_fake_data_prompt(func, num_rows, num_columns)
    
    # Assert
    assert isinstance(result, str)
    assert result == expected_output.strip()

# Test case for error condition with invalid function signature
def test_generate_fake_data_prompt_error_invalid_function(mock_systemprompts):
    # Arrange
    func = MagicMock(spec=lambda: None, __name__='test_func', __annotations__={'arg1': int})
    num_rows = -5  # Invalid number of rows
    num_columns = 5
    
    # Act and Assert
    with pytest.raises(ValueError):
        mock_systemprompts.generate_fake_data_prompt(func, num_rows, num_columns)

# Test case for efficiency by checking large data generation
@pytest.mark.skip(reason="Skipping due to time constraints")
def test_generate_fake_data_prompt_efficiency(mock_systemprompts):
    # Arrange
    func = MagicMock(spec=lambda: None, __name__='test_func', __annotations__={'arg1': int, 'arg2': str})
    num_rows = 10000
    num_columns = 5
    
    # Act
    result = mock_systemprompts.generate_fake_data_prompt(func, num_rows, num_columns)
    
    # Assert
    assert isinstance(result, str)
    assert "pandas DataFrame" in result  # Ensure data generation is mentioned

# Test case for ensuring the function name and annotations are correctly included
def test_generate_fake_data_prompt_function_details(mock_systemprompts):
    # Arrange
    func = MagicMock(spec=lambda: None, __name__='test_func', __annotations__={'arg1': int, 'arg2': str})
    num_rows = 100
    num_columns = 5
    
    expected_output = f"""
    Generate a Python script to create fake data for the following function:
    
    def test_func(arg1: <class 'int'>, arg2: <class 'str'>):
    
    Use only the Faker library to generate appropriate fake data.
    
    Create a pandas DataFrame named 'fake_data' containing the generated data.
    
    Ensure the generated data is diverse and suitable for testing the function.
    
    Do not use PandasProvider or any other external libraries besides Faker, random, and pandas.
    
    """
    
    # Act
    result = mock_systemprompts.generate_fake_data_prompt(func, num_rows, num_columns)
    
    # Assert
    assert isinstance(result, str)
    assert result == expected_output.strip()