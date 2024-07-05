# Updated Implementation of FunctionAttributesFactory._get_class_and_method_names function

def _get_class_and_method_names(func_name: str) -> tuple[str, str]:
    parts = func_name.split(".")
    if len(parts) > 1:
        return (".".join(parts[:-1]), parts[-1])
    else:
        return ("", func_name)

from unittest.mock import patch

import pytest
from code_autoeval.clients.llm_model.utils.model.function_attributes import FunctionAttributesFactory

# Test cases for _get_class_and_method_names function

def test_normal_case():
    func_name = "module.Class.method"
    expected_output = ("module.Class", "method")
    assert FunctionAttributesFactory._get_class_and_method_names(func_name) == expected_output

def test_no_dot_in_function_name():
    func_name = "method"
    expected_output = ("", "method")
    assert FunctionAttributesFactory._get_class_and_method_names(func_name) == expected_output

def test_empty_string():
    func_name = ""
    expected_output = ("", "")
    assert FunctionAttributesFactory._get_class_and_method_names(func_name) == expected_output

def test_single_part_function_name():
    func_name = "module"
    expected_output = ("", "module")
    assert FunctionAttributesFactory._get_class_and_method_names(func_name) == expected_output

def test_multiple_dots_in_middle():
    func_name = "module.Class.submodule.method"
    expected_output = ("module.Class.submodule", "method")
    assert FunctionAttributesFactory._get_class_and_method_names(func_name) == expected_output