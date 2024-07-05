import asyncio
import inspect
from unittest.mock import MagicMock, patch

import pytest
from code_autoeval.clients.llm_model.utils.model.function_attributes import FunctionAttributesFactory

# Analysis of the function _is_coroutine:
# The function checks if a given function is a coroutine by using asyncio.iscoroutinefunction and inspect.iscoroutinefunction.
# If a ClassDataModel is provided, it also checks if the method name is in its coroutine_methods attribute.

def test_is_coroutine_normal():
    # Test normal use case where func is a coroutine function
    async def mock_coroutine():
        pass
    
    with patch('asyncio.iscoroutinefunction', return_value=True):
        result = FunctionAttributesFactory._is_coroutine(mock_coroutine)
        assert result == True

def test_is_coroutine_not_coroutine():
    # Test case where func is not a coroutine function
    def mock_function():
        pass
    
    with patch('asyncio.iscoroutinefunction', return_value=False):
        result = FunctionAttributesFactory._is_coroutine(mock_function)
        assert result == False

def test_is_coroutine_with_class_model():
    # Test case where a ClassDataModel is provided and the method name is in coroutine_methods
    class ClassDataModel:
        def __init__(self):
            self.coroutine_methods = {'method1'}
    
    async def mock_coroutine():
        pass
    
    with patch('asyncio.iscoroutinefunction', return_value=False), \
         patch('inspect.iscoroutinefunction', return_value=False):
        result = FunctionAttributesFactory._is_coroutine(mock_coroutine, ClassDataModel())
        assert result == True

def test_is_coroutine_not_in_class_model():
    # Test case where a ClassDataModel is provided but the method name is not in coroutine_methods
    class ClassDataModel:
        def __init__(self):
            self.coroutine_methods = {'other_method'}
    
    async def mock_coroutine():
        pass
    
    with patch('asyncio.iscoroutinefunction', return_value=False), \
         patch('inspect.iscoroutinefunction', return_value=False):
        result = FunctionAttributesFactory._is_coroutine(mock_coroutine, ClassDataModel())
        assert result == False

def test_is_coroutine_no_class_model():
    # Test case where no ClassDataModel is provided
    async def mock_coroutine():
        pass
    
    with patch('asyncio.iscoroutinefunction', return_value=True), \
         patch('inspect.iscoroutinefunction', return_value=False):
        result = FunctionAttributesFactory._is_coroutine(mock_coroutine)
        assert result == True