# Updated Implementation of FunctionAttributesFactory._get_class_and_method_names function.

def _get_class_and_method_names(func_name: str) -> tuple[str, str]:
    if not isinstance(func_name, str):
        raise TypeError("Input must be a string")
    
    parts = func_name.split(".")
    return (".".join(parts[:-1]), parts[-1]) if len(parts) > 1 else ("", func_name)

from unittest.mock import patch

import pytest


def _get_class_and_method_names(func_name: str) -> tuple[str, str]:
    if not isinstance(func_name, str):
        raise TypeError("Input must be a string")
    
    parts = func_name.split(".")
    return (".".join(parts[:-1]), parts[-1]) if len(parts) > 1 else ("", func_name)

##################################################
# TESTS
##################################################

def test_normal_case():
    # Test normal use case with a simple function name
    assert _get_class_and_method_names("module.Class.method") == ("module.Class", "method")

def test_no_class_case():
    # Test when there is no class (only method)
    assert _get_class_and_method_names("module.method") == ("module", "method")

def test_empty_string():
    # Test with an empty string
    assert _get_class_and_method_names("") == ("", "")

def test_single_part_function():
    # Test when the function name is just a method (no class or module)
    assert _get_class_and_method_names("method") == ("", "method")

def test_none_input():
    # Test with None input, which should raise a TypeError
    with pytest.raises(TypeError):
        _get_class_and_method_names(None)

def test_non_string_input():
    # Test with non-string input, which should raise a TypeError
    with pytest.raises(TypeError):
        _get_class_and_method_names(12345)

def test_multiple_dots():
    # Test when there are multiple dots in the function name
    assert _get_class_and_method_names("module.submodule.Class.method") == ("module.submodule.Class", "method")

def test_trailing_dot():
    # Test when the function name ends with a dot
    assert _get_class_and_method_names("module.Class.") == ("module.Class", "")