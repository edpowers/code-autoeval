from unittest.mock import patch

import pytest

from code_autoeval.llm_model.utils.execute_generated_code import ExecuteGeneratedCode


def test_normal_case():
    # Arrange
    func = lambda x: x + 1
    local_vars = {"func": func}
    expected_output = "func"

    # Act
    with patch(
        "code_autoeval.llm_model.utils.execute_generated_code.ExecuteGeneratedCode._find_func_name",
        return_value=expected_output,
    ):
        result = ExecuteGeneratedCode()._find_func_name(func, local_vars)

    # Assert
    assert result == expected_output


def test_function_not_in_local_vars():
    # Arrange
    func = lambda x: x + 1
    local_vars = {"other_func": lambda y: y * 2}

    # Act & Assert
    with pytest.raises(ValueError):
        ExecuteGeneratedCode()._find_func_name(func, local_vars)


def test_function_not_callable():
    # Arrange
    func = "not callable"
    local_vars = {"non_callable": func}

    # Act & Assert
    with pytest.raises(ValueError):
        ExecuteGeneratedCode()._find_func_name(func, local_vars)  # Act & Assert
    with pytest.raises(ValueError):
        ExecuteGeneratedCode()._find_func_name(func, local_vars)
