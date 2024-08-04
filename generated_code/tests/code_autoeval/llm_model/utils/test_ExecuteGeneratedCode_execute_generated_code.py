from unittest.mock import MagicMock

import pandas
import pandas as pd
import pytest
from code_autoeval.llm_model.utils.execute_generated_code import ExecuteGeneratedCode


@pytest.fixture(scope='module')
def mock_executegeneratedcode():
    return ExecuteGeneratedCode()

def test_ExecuteGeneratedCode_execute_generated_code_normal_use_case(mock_executegeneratedcode):
    # Arrange
    self = MagicMock()
    original_code = "print('Hello, World!')"
    func_attributes = MagicMock()
    df = pd.DataFrame({'A': range(10), 'B': range(10, 20)})
    debug = False
    class_model = None

    instance = mock_executegeneratedcode

    # Act
    result, context = instance.execute_generated_code(self, original_code, func_attributes, df, debug, class_model)

    # Assert
    assert isinstance(result, str)
    assert result == "Hello, World!"
    assert isinstance(context, dict)
    assert 'df' not in context  # Ensure the DataFrame is not included in the context

def test_ExecuteGeneratedCode_execute_generated_code_with_class_model(mock_executegeneratedcode):
    # Arrange
    self = MagicMock()
    original_code = "print('Hello, World!')"
    func_attributes = MagicMock()
    df = pd.DataFrame({'A': range(10), 'B': range(10, 20)})
    debug = False
    class_model = MagicMock()

    instance = mock_executegeneratedcode

    # Act
    result, context = instance.execute_generated_code(self, original_code, func_attributes, df, debug, class_model)

    # Assert
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)
    assert 'df' not in context  # Ensure the DataFrame is not included in the context when class_model is provided

def test_ExecuteGeneratedCode_execute_generated_code_with_empty_dataframe(mock_executegeneratedcode):
    # Arrange
    self = MagicMock()
    original_code = "print('Hello, World!')"
    func_attributes = MagicMock()
    df = pd.DataFrame({'A': [], 'B': []})  # Empty DataFrame
    debug = False
    class_model = None

    instance = mock_executegeneratedcode

    # Act
    result, context = instance.execute_generated_code(self, original_code, func_attributes, df, debug, class_model)

    # Assert
    assert isinstance(result, str)
    assert result == "Hello, World!"
    assert isinstance(context, dict)
    assert 'df' not in context  # Ensure the DataFrame is not included in the context even if it's empty

def test_ExecuteGeneratedCode_execute_generated_code_with_exception(mock_executegeneratedcode):
    # Arrange
    self = MagicMock()
    original_code = "raise ValueError('Test exception')"  # Code that raises an exception
    func_attributes = MagicMock()
    df = pd.DataFrame({'A': range(10), 'B': range(10, 20)})
    debug = False
    class_model = None

    instance = mock_executegeneratedcode

    # Act & Assert
    with pytest.raises(ValueError):
        result, context = instance.execute_generated_code(self, original_code, func_attributes, df, debug, class_model)