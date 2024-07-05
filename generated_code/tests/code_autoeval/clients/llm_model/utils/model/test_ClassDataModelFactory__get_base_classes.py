# Updated Implementation of ClassDataModelFactory._get_base_classes function
from typing import Any, List


class ClassDataModelFactory:
    @staticmethod
    def _get_base_classes(class_to_process: Any) -> List[str]:
        if not isinstance(class_to_process, type):
            raise ValueError("Input must be a class type")
        return [base.__name__ for base in class_to_process.__bases__]

# Updated Implementation of ClassDataModelFactory._get_base_classes function
from typing import Any, List


class ClassDataModelFactory:
    @staticmethod
    def _get_base_classes(class_to_process: Any) -> List[str]:
        if not isinstance(class_to_process, type):
            raise ValueError("Input must be a class type")
        return [base.__name__ for base in class_to_process.__bases__]

from typing import List
from unittest.mock import patch

import pytest


# Updated implementation of ClassDataModelFactory._get_base_classes function
class ClassDataModelFactory:
    @staticmethod
    def _get_base_classes(class_to_process: Any) -> List[str]:
        if not isinstance(class_to_process, type):
            raise ValueError("Input must be a class type")
        return [base.__name__ for base in class_to_process.__bases__]

# Test the function with normal case
@patch("code_autoeval.clients.llm_model.utils.model.class_data_model.ClassDataModelFactory._get_base_classes")
def test_normal_case(mock_get_base_classes):
    # Arrange
    class MockClass:
        pass
    
    mock_bases = [MockClass, object]
    mock_get_base_classes.return_value = ['MockClass', 'object']
    
    # Act
    result = ClassDataModelFactory._get_base_classes(MockClass)
    
    # Assert
    assert result == ['MockClass', 'object']

# Test the function with no base classes
def test_no_bases():
    # Arrange
    class NoBaseClass:
        pass
    
    # Act
    result = ClassDataModelFactory._get_base_classes(NoBaseClass)
    
    # Assert
    assert result == []

# Test the function with a single base class
def test_single_base():
    # Arrange
    class SingleBaseClass(object):
        pass
    
    # Act
    result = ClassDataModelFactory._get_base_classes(SingleBaseClass)
    
    # Assert
    assert result == ['object']

# Test the function with multiple base classes
def test_multiple_bases():
    # Arrange
    class Base1:
        pass
    
    class Base2(Base1):
        pass
    
    class MultipleBases(Base2, object):
        pass
    
    # Act
    result = ClassDataModelFactory._get_base_classes(MultipleBases)
    
    # Assert
    assert result == ['Base2', 'Base1', 'object']

# Test the function with invalid input (non-class type)
def test_invalid_input():
    # Arrange
    with pytest.raises(ValueError):
        ClassDataModelFactory._get_base_classes("NotAClass")