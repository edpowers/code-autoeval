from unittest.mock import MagicMock, patch

import pytest

from code_autoeval.llm_model.utils.model.function_attributes import (
    FunctionAttributesFactory,
)


def test_normal_use_case():
    # Arrange
    func = lambda x: x + 1
    class_model = MagicMock()
    class_model.class_name = "TestClass"

    # Act
    result = FunctionAttributesFactory._get_function_name(func, class_model)

    # Assert
    assert result == "TestClass.lambda"


def test_no_class_model():
    # Arrange
    func = lambda x: x + 1

    # Act
    result = FunctionAttributesFactory._get_function_name(func)

    # Assert
    assert result == "lambda"


def test_with_non_string_class_name():
    # Arrange
    func = lambda x: x + 1
    class_model = MagicMock()
    class_model.class_name = None

    # Act
    result = FunctionAttributesFactory._get_function_name(func, class_model)

    # Assert
    assert result == "lambda"
    # Assert
    assert result == "lambda"
