import pathlib
from typing import Callable, ForwardRef, Optional
from unittest.mock import patch

from code_autoeval.llm_model.utils.model.class_data_model import ClassDataModel
from code_autoeval.llm_model.utils.model.function_attributes import (
    FunctionAttributes,
    FunctionAttributesFactory,
)


def create(
    func: Callable,
    generated_base_dir: pathlib.Path,
    class_model: Optional[ForwardRef("ClassDataModel")] = None,
) -> FunctionAttributes:
    """
    Extract all relevant attributes from a given function and create a FunctionAttributes instance.

    Args:
        func (Callable): The function to extract attributes from.
        generated_base_dir (Path): The base directory where the test files will be generated.
        class_model (Optional[ClassDataModel]): The class model if the function is a method.

    Returns:
        FunctionAttributes: A model containing all extracted function attributes.
    """
    func_name = FunctionAttributesFactory._get_function_name(func, class_model)
    class_name, method_name = FunctionAttributesFactory._get_class_and_method_names(
        func_name
    )

    test_relative_file_path, test_absolute_file_path = (
        FunctionAttributesFactory._construct_file_paths(
            func_name,
            class_model.module_relative_path if class_model else None,
            generated_base_dir,
        )
    )

    return FunctionAttributes(
        func_name=func_name,
        function_signature=FunctionAttributesFactory._get_function_signature(func),
        function_docstring=FunctionAttributesFactory._get_function_docstring(func),
        function_body=FunctionAttributesFactory._get_function_body(func),
        class_name=class_name,
        method_name=method_name,
        is_coroutine=FunctionAttributesFactory._is_coroutine(
            func, class_model, method_name
        ),
        module_absolute_path=class_model.module_absolute_path if class_model else None,
        module_relative_path=class_model.module_relative_path if class_model else None,
        test_relative_file_path=test_relative_file_path,
        test_absolute_file_path=test_absolute_file_path,
    )


import pathlib
from typing import Callable, ForwardRef, Optional
from unittest.mock import patch

import pytest

from code_autoeval.llm_model.utils.model.class_data_model import ClassDataModel
from code_autoeval.llm_model.utils.model.function_attributes import (
    FunctionAttributesFactory,
)


@pytest.fixture
def mock_func():
    def example_func(arg1: int, arg2: int) -> int:
        return arg1 + arg2

    return example_func


@pytest.fixture
def mock_class_model():
    class MockClassDataModel:
        module_absolute_path = "mock_module"
        module_relative_path = "mock_module"

    return MockClassDataModel()


@patch(
    "code_autoeval.llm_model.utils.model.function_attributes.FunctionAttributesFactory._get_function_name"
)
def test_create_normal(mock_get_func_name, mock_func, mock_class_model):
    mock_get_func_name.return_value = "example_func"
    generated_base_dir = pathlib.Path("test_dir")

    result = FunctionAttributesFactory.create(
        mock_func, generated_base_dir, mock_class_model
    )

    assert result.func_name == "example_func"
    assert result.function_signature is not None
    assert result.function_docstring is not None
    assert result.function_body is not None
    assert result.class_name is None
    assert result.method_name is None
    assert result.is_coroutine == False
    assert result.module_absolute_path == "mock_module"
    assert result.module_relative_path == "mock_module"
    assert result.test_relative_file_path is not None
    assert result.test_absolute_file_path is not None


@patch(
    "code_autoeval.llm_model.utils.model.function_attributes.FunctionAttributesFactory._get_function_name"
)
def test_create_method(mock_get_func_name, mock_func, mock_class_model):
    mock_get_func_name.return_value = "MockClass.example_method"
    generated_base_dir = pathlib.Path("test_dir")

    result = FunctionAttributesFactory.create(
        mock_func, generated_base_dir, mock_class_model
    )

    assert result.func_name == "MockClass.example_method"
    assert result.function_signature is not None
    assert result.function_docstring is not None
    assert result.function_body is not None
    assert result.class_name == "MockClass"
    assert result.method_name == "example_method"
    assert result.is_coroutine == False
    assert result.module_absolute_path == "mock_module"
    assert result.module_relative_path == "mock_module"
    assert result.test_relative_file_path is not None
    assert result.test_absolute_file_path is not None


def test_create_no_class_model(mock_func):
    generated_base_dir = pathlib.Path("test_dir")

    with pytest.raises(TypeError):
        FunctionAttributesFactory.create(mock_func, generated_base_dir)
    with pytest.raises(TypeError):
        FunctionAttributesFactory.create(mock_func, generated_base_dir)
