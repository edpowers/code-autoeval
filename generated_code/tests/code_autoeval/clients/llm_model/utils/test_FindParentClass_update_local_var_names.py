from unittest.mock import MagicMock, patch

import pytest
from code_autoeval.clients.llm_model.utils.find_parent_class import FindParentClass

# Function Analysis:
# The function `update_local_var_names` is designed to update local variable names in a dictionary by mapping them to the _func_name attribute of classes if such an attribute exists. If not, it keeps the original key.

def test_normal_use():
    # Arrange
    local_vars = {
        'ClassA': type('ClassA', (object,), {'_func_name': 'FuncNameA'}),
        'ClassB': type('ClassB', (object,), {})
    }
    
    expected_output = {
        'FuncNameA': local_vars['ClassA'],
        'ClassB': local_vars['ClassB']
    }
    
    # Act
    with patch("code_autoeval.clients.llm_model.utils.find_parent_class.FindParentClass._func_name", create=True) as mock_func_name:
        mock_func_name.__get__ = MagicMock(return_value='FuncNameA')
        result = FindParentClass.update_local_var_names(None, local_vars)
    
    # Assert
    assert result == expected_output

def test_no_func_name():
    # Arrange
    local_vars = {
        'ClassC': type('ClassC', (object,), {})
    }
    
    expected_output = {
        'ClassC': local_vars['ClassC']
    }
    
    # Act
    result = FindParentClass.update_local_var_names(None, local_vars)
    
    # Assert
    assert result == expected_output

def test_empty_dict():
    # Arrange
    local_vars = {}
    
    expected_output = {}
    
    # Act
    result = FindParentClass.update_local_var_names(None, local_vars)
    
    # Assert
    assert result == expected_output

def test_mixed_types():
    # Arrange
    local_vars = {
        'ClassD': type('ClassD', (object,), {'_func_name': 'FuncNameD'}),
        123: "not a class"
    }
    
    expected_output = {
        'FuncNameD': local_vars['ClassD'],
        123: "not a class"
    }
    
    # Act
    result = FindParentClass.update_local_var_names(None, local_vars)
    
    # Assert
    assert result == expected_output

def test_none_input():
    # Arrange
    local_vars = None
    
    # Act & Assert
    with pytest.raises(TypeError):
        FindParentClass.update_local_var_names(None, local_vars)