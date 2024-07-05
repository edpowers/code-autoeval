import inspect
import pathlib
from typing import Callable, ForwardRef, Optional
from unittest.mock import MagicMock, patch

import pytest


class ClassDataModel:
    def __init__(self, module_absolute_path: str, module_relative_path: str):
        self.module_absolute_path = module_absolute_path
        self.module_relative_path = module_relative_path

class FunctionAttributesFactory:
    @staticmethod
    def create(func: Callable, generated_base_dir: pathlib.Path, class_model: Optional[ClassDataModel] = None) -> 'FunctionAttributes':
        func_name = FunctionAttributesFactory._get_function_name(func, class_model)
        class_name, method_name = FunctionAttributesFactory._get_class_and_method_names(func_name)
        test_relative_file_path, test_absolute_file_path = (
            FunctionAttributesFactory._construct_file_paths(
                func_name, class_model.module_relative_path, generated_base_dir
            )
        )
        return FunctionAttributes(
            func_name=func_name,
            function_signature=FunctionAttributesFactory._get_function_signature(func),
            function_docstring=FunctionAttributesFactory._get_function_docstring(func),
            function_body=FunctionAttributesFactory._get_function_body(func),
            class_name=class_name,
            method_name=method_name,
            is_coroutine=FunctionAttributesFactory._is_coroutine(func, class_model, method_name),
            module_absolute_path=class_model.module_absolute_path if class_model else None,
            module_relative_path=class_model.module_relative_path if class_model else None,
            test_relative_file_path=test_relative_file_path,
            test_absolute_file_path=test_absolute_file_path,
        )

    @staticmethod
    def _get_function_name(func: Callable, class_model: Optional[ClassDataModel] = None) -> str:
        if class_model and func.__name__ != '__init__':
            return f"{class_model.module_relative_path}.{func.__name__}"
        return func.__name__

    @staticmethod
    def _get_class_and_method_names(func_name: str) -> tuple[str, str]:
        parts = func_name.split('.')
        if len(parts) > 1 and parts[-1] != '__init__':
            return (parts[-2], parts[-1])
        return ('', '')

    @staticmethod
    def _construct_file_paths(func_name: str, module_relative_path: str, generated_base_dir: pathlib.Path) -> tuple[str, str]:
        test_relative_file_path = f"test_{module_relative_path}" if module_relative_path else "test"
        test_absolute_file_path = generated_base_dir / f"{func_name.replace('.', '/')}_test.py"
        return (test_relative_file_path, str(test_absolute_file_path))

    @staticmethod
    def _get_function_signature(func: Callable) -> str:
        return inspect.signature(func)

    @staticmethod
    def _get_function_docstring(func: Callable) -> Optional[str]:
        return func.__doc__

    @staticmethod
    def _get_function_body(func: Callable) -> str:
        return inspect.getsource(func)

    @staticmethod
    def _is_coroutine(func: Callable, class_model: Optional[ClassDataModel], method_name: str) -> bool:
        if func.__module__ == 'asyncio':
            return True
        if class_model and method_name != '__init__':
            return asyncio.iscoroutinefunction(func)
        return False

class FunctionAttributes:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

import asyncio
import inspect
import pathlib
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_function():
    def example_func(arg1: int, arg2: int) -> int:
        return arg1 + arg2
    return example_func

@pytest.fixture
def mock_class_model():
    return ClassDataModel("module.path", "relative.path")

@pytest.fixture
def generated_base_dir():
    return pathlib.Path("/test/base/dir")

@patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory._get_function_name", return_value="module.path.example_func")
@patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory._get_class_and_method_names", return_value=("", ""))
@patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory._construct_file_paths", return_value=("test_relative_path", "/test/base/dir/module.path.example_func_test.py"))
@patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory._get_function_signature", return_value="inspect.Signature")
@patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory._get_function_docstring", return_value="Example docstring")
@patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory._get_function_body", return_value="def example_func(arg1, arg2): return arg1 + arg2")
@patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory._is_coroutine", return_value=False)
def test_create_normal_case(mock_is_coroutine, mock_get_function_body, mock_get_function_docstring, mock_get_function_signature, mock_construct_file_paths, mock_get_class_and_method_names, mock_get_function_name):
    func = MagicMock()
    class_model = MagicMock()
    result = FunctionAttributesFactory.create(func, generated_base_dir(), class_model)
    assert result.func_name == "module.path.example_func"
    assert result.function_signature == "inspect.Signature"
    assert result.function_docstring == "Example docstring"
    assert result.function_body == "def example_func(arg1, arg2): return arg1 + arg2"
    assert result.class_name == ""
    assert result.method_name == ""
    assert not result.is_coroutine
    assert result.module_absolute_path == class_model.module_absolute_path
    assert result.module_relative_path == class_model.module_relative_path
    assert result.test_relative_file_path == "test_relative_path"
    assert result.test_absolute_file_path == "/test/base/dir/module.path.example_func_test.py"

def test_create_method_case(mock_function, mock_class_model, generated_base_dir):
    class_model = ClassDataModel("module.path", "relative.path")
    func = mock_function
    result = FunctionAttributesFactory.create(func, generated_base_dir(), class_model)
    assert result.func_name == "module.path.example_func"
    assert result.class_name == "ClassDataModel"
    assert result.method_name == "example_func"

def test_create_coroutine_case(mock_function, generated_base_dir):
    async def coroutine_func():
        pass
    class_model = None
    with patch('asyncio.iscoroutinefunction', return_value=True):
        result = FunctionAttributesFactory.create(coroutine_func, generated_base_dir(), class_model)
        assert result.is_coroutine

def test_create_no_class_model_case():
    def func():
        pass
    class_model = None
    result = FunctionAttributesFactory.create(func, pathlib.Path("/test/base/dir"), class_model)
    assert result.module_absolute_path is None
    assert result.module_relative_path is None

def test_create_error_case():
    def func():
        raise ValueError("Test error")
    class_model = MagicMock()
    with pytest.raises(ValueError):
        FunctionAttributesFactory.create(func, pathlib.Path("/test/base/dir"), class_model)