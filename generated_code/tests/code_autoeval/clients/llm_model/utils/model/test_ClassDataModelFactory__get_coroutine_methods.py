import inspect
from typing import Any, List
from unittest.mock import MagicMock, patch

import pytest
from code_autoeval.clients.llm_model.utils.model.class_data_model import ClassDataModelFactory


# Mocking the dependencies as per the instructions
@patch("code_autoeval.clients.llm_model.utils.model.class_data_model.ClassDataModelFactory.__init__", return_value=None)
def test_get_coroutine_methods(mock_init):
    class TestClass:
        def __init__(self, project_root):
            pass
        
        async def coroutine_method(self):
            pass
        
        async def another_coroutine_method(self):
            pass
        
        def regular_method(self):
            pass
    
    test_instance = TestClass()
    result = ClassDataModelFactory._get_coroutine_methods(test_instance)
    assert len(result) == 2
    assert 'coroutine_method' in result
    assert 'another_coroutine_method' in result

def test_no_coroutine_methods():
    class TestClass:
        def __init__(self, project_root):
            pass
        
        def regular_method(self):
            pass
    
    test_instance = TestClass()
    result = ClassDataModelFactory._get_coroutine_methods(test_instance)
    assert len(result) == 0

def test_class_with_async_gen_methods():
    class TestClass:
        def __init__(self, project_root):
            pass
        
        async def coroutine_method(self):
            pass
        
        async def another_coroutine_method(self):
            pass
        
        async def async_gen_method(self):
            yield 1
        
    test_instance = TestClass()
    result = ClassDataModelFactory._get_coroutine_methods(test_instance)
    assert len(result) == 3
    assert 'coroutine_method' in result
    assert 'another_coroutine_method' in result
    assert 'async_gen_method' in result

def test_none_input():
    with pytest.raises(TypeError):
        ClassDataModelFactory._get_coroutine_methods(None)

def test_non_class_input():
    with pytest.raises(TypeError):
        ClassDataModelFactory._get_coroutine_methods("not a class")