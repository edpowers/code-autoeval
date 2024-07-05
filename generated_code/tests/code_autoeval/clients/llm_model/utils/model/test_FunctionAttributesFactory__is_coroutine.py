import asyncio
import inspect
from unittest.mock import MagicMock, patch

import pytest

from code_autoeval.llm_model.utils.model.function_attributes import \
    FunctionAttributesFactory


def test_is_coroutine_normal():
    # Test normal use case where the function is a coroutine
    async def mock_coroutine():
        pass

    func = mock_coroutine
    result = FunctionAttributesFactory._is_coroutine(func, None, "mock_method")
    assert result == True

def test_is_coroutine_not_coroutine():
    # Test case where the function is not a coroutine
    def mock_function():
        pass

    func = mock_function
    result = FunctionAttributesFactory._is_coroutine(func, None, "mock_method")
    assert result == False

def test_is_coroutine_with_class_model():
    # Test case where the function is a coroutine and it's in the class model's coroutine methods list
    async def mock_coroutine():
        pass

    func = mock_coroutine
    class_model = MagicMock()
    class_model.coroutine_methods = {"mock_method"}
    result = FunctionAttributesFactory._is_coroutine(func, class_model, "mock_method")
    assert result == True

def test_is_coroutine_not_in_class_model():
    # Test case where the function is a coroutine but it's not in the class model's coroutine methods list
    async def mock_coroutine():
        pass

    func = mock_coroutine
    class_model = MagicMock()
    class_model.coroutine_methods = {"other_method"}
    result = FunctionAttributesFactory._is_coroutine(func, class_model, "mock_method")
    assert result == False

def test_is_coroutine_none_class_model():
    # Test case where the class model is None
    async def mock_coroutine():
        pass

    func = mock_coroutine
    result = FunctionAttributesFactory._is_coroutine(func, None, "mock_method")
    assert result == False    func = mock_coroutine
    result = FunctionAttributesFactory._is_coroutine(func, None, "mock_method")
    assert result == False