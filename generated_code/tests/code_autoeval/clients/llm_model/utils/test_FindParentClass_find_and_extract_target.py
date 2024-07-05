import ast
from typing import Tuple
from unittest.mock import MagicMock, patch

import astor
import pytest


class FindParentClass:
    def find_and_extract_target(self, code: str, target_name: str) -> Tuple[str, str]:
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

##################################################
# TESTS
##################################################

@patch("code_autoeval.clients.llm_model.utils.find_parent_class.FindParentClass")
def test_normal_case(mock_find_parent_class):
    # Arrange
    mock_instance = mock_find_parent_class.return_value
    code = "class Parent: def target(): pass"
    expected_source = "def target():\n    pass\n"
    expected_parent_class = "Parent"
    mock_instance.find_and_extract_target.return_value = (expected_source, expected_parent_class)

    # Act
    source, parent_class = mock_instance.find_and_extract_target(code, "target")

    # Assert
    assert source == expected_source
    assert parent_class == expected_parent_class

@patch("code_autoeval.clients.llm_model.utils.find_parent_class.FindParentClass")
def test_no_parent_class(mock_find_parent_class):
    # Arrange
    mock_instance = mock_find_parent_class.return_value
    code = "def target(): pass"
    expected_source = "def target():\n    pass\n"
    mock_instance.find_and_extract_target.return_value = (expected_source, None)

    # Act
    source, parent_class = mock_instance.find_and_extract_target(code, "target")

    # Assert
    assert source == expected_source
    assert parent_class is None

@patch("code_autoeval.clients.llm_model.utils.find_parent_class.FindParentClass")
def test_no_target(mock_find_parent_class):
    # Arrange
    mock_instance = mock_find_parent_class.return_value
    code = "class Parent: pass"
    expected_source = None
    expected_parent_class = None
    mock_instance.find_and_extract_target.return_value = (expected_source, expected_parent_class)

    # Act
    source, parent_class = mock_instance.find_and_extract_target(code, "non_existent")

    # Assert
    assert source == expected_source
    assert parent_class == expected_parent_class

@patch("code_autoeval.clients.llm_model.utils.find_parent_class.FindParentClass")
def test_multiple_targets(mock_find_parent_class):
    # Arrange
    mock_instance = mock_find_parent_class.return_value
    code = "class Parent: def target(): pass; def another_target(): pass"
    expected_source = "def target():\n    pass\n"
    expected_parent_class = "Parent"
    mock_instance.find_and_extract_target.return_value = (expected_source, expected_parent_class)

    # Act
    source, parent_class = mock_instance.find_and_extract_target(code, "target")

    # Assert
    assert source == expected_source
    assert parent_class == expected_parent_class

@patch("code_autoeval.clients.llm_model.utils.find_parent_class.FindParentClass")
def test_method_in_nested_class(mock_find_parent_class):
    # Arrange
    mock_instance = mock_find_parent_class.return_value
    code = "class Parent: class Nested: def target(): pass"
    expected_source = "def target():\n    pass\n"
    expected_parent_class = "Parent.Nested"
    mock_instance.find_and_extract_target.return_value = (expected_source, expected_parent_class)

    # Act
    source, parent_class = mock_instance.find_and_extract_target(code, "target")

    # Assert
    assert source == expected_source
    assert parent_class == expected_parent_class