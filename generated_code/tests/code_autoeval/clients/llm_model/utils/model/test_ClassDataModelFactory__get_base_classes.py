# Updated Implementation of ClassDataModelFactory._get_base_classes function
from typing import Any, List


def _get_base_classes(class_to_process: Any) -> List[str]:
    if not isinstance(class_to_process, type):
        raise TypeError("Input must be a class type")
    return [base.__name__ for base in class_to_process.__bases__]

from unittest.mock import patch

# Comprehensive Set of pytest Tests
import pytest


def _get_base_classes(class_to_process: Any) -> List[str]:
    if not isinstance(class_to_process, type):
        raise TypeError("Input must be a class type")
    return [base.__name__ for base in class_to_process.__bases__]

# Test the function
@pytest.mark.asyncio
async def test_normal_case():
    # Arrange
    class MockClass(object): pass
    
    mock_class = MockClass()
    expected_output = ['object']
    
    # Act
    result = await _get_base_classes(mock_class)
    
    # Assert
    assert result == expected_output

@pytest.mark.asyncio
async def test_no_bases():
    # Arrange
    class MockClass: pass
    
    mock_class = MockClass()
    expected_output = []
    
    # Act
    result = await _get_base_classes(mock_class)
    
    # Assert
    assert result == expected_output

@pytest.mark.asyncio
async def test_multiple_bases():
    # Arrange
    class Base1: pass
    class Base2: pass
    class MockClass(Base1, Base2): pass
    
    mock_class = MockClass()
    expected_output = ['Base1', 'Base2']
    
    # Act
    result = await _get_base_classes(mock_class)
    
    # Assert
    assert result == expected_output

@pytest.mark.asyncio
async def test_none():
    # Arrange
    mock_class = None
    
    # Act and Assert
    with pytest.raises(TypeError):
        await _get_base_classes(mock_class)

@pytest.mark.asyncio
async def test_non_type():
    # Arrange
    mock_class = "not a class"
    
    # Act and Assert
    with pytest.raises(AttributeError):
        await _get_base_classes(mock_class)

@pytest.mark.asyncio
async def test_non_class():
    # Arrange
    mock_class = 12345
    
    # Act and Assert
    with pytest.raises(TypeError):
        await _get_base_classes(mock_class)