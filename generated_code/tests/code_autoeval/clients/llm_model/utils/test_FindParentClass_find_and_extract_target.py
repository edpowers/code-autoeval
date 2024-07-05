import ast
from typing import Optional, Tuple

import astor


class FindParentClass:
    def find_and_extract_target(self, code: str, target_name: str) -> Tuple[str, Optional[str]]:
        """
        Parse the code, find the target function or class, and extract its source along with its parent class if it's a method.

        :param code: The code string to parse
        :param target_name: The name of the function or class to find
        :return: A tuple (source code of the target, parent class name if it's a method, else None)
        """
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for child in node.body:
                    if isinstance(child, ast.FunctionDef) and child.name == target_name:
                        return astor.to_source(child), node.name
            elif isinstance(node, ast.FunctionDef) and node.name == target_name:
                return astor.to_source(node), None

        return None, None

import ast
from unittest.mock import patch

import astor
import pytest

from code_autoeval.llm_model.utils.find_parent_class import FindParentClass


@pytest.fixture
def find_parent_class():
    return FindParentClass()

def test_find_and_extract_target_function(find_parent_class):
    code = """
def my_function():
    pass
"""
    target_name = "my_function"
    result, parent_class = find_parent_class.find_and_extract_target(code, target_name)
    assert result == 'def my_function():\n    pass\n'
    assert parent_class is None

def test_find_and_extract_target_method(find_parent_class):
    code = """
class MyClass:
    def my_method(self):
        pass
"""
    target_name = "my_method"
    result, parent_class = find_parent_class.find_and_extract_target(code, target_name)
    assert result == 'def my_method(self):\n    pass\n'
    assert parent_class == "MyClass"

def test_find_and_extract_target_not_found(find_parent_class):
    code = """
def another_function():
    pass
"""
    target_name = "my_method"
    result, parent_class = find_parent_class.find_and_extract_target(code, target_name)
    assert result is None
    assert parent_class is None

def test_find_and_extract_target_empty_code(find_parent_class):
    code = ""
    target_name = "my_function"
    result, parent_class = find_parent_class.find_and_extract_target(code, target_name)
    assert result is None
    assert parent_class is None

def test_find_and_extract_target_invalid_input(find_parent_class):
    code = "invalid input"
    target_name = "my_function"
    with pytest.raises(SyntaxError):
        find_parent_class.find_and_extract_target(code, target_name)

def my_function():
    pass    pass