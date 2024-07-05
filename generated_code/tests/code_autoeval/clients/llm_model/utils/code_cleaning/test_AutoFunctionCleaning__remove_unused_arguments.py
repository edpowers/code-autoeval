import ast
from unittest.mock import MagicMock, patch

import astor
import pytest


class AutoFunctionCleaning:
    def _remove_unused_arguments(self, source_code: str) -> str:
        class UnusedArgumentRemover(ast.NodeTransformer):
            def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
                arg_names = {arg.arg for arg in node.args.args}
                used_names = {child.id for child in ast.walk(node) if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load)}
                unused_args = arg_names - used_names
                node.args.args = [arg for arg in node.args.args if arg.arg not in unused_args]
                return node
        
        tree = ast.parse(source_code)
        transformer = UnusedArgumentRemover()
        modified_tree = transformer.visit(tree)
        return astor.to_source(modified_tree)

# Analysis:
# The function _remove_unused_arguments takes a string of source code, parses it into an Abstract Syntax Tree (AST), 
# identifies and removes unused arguments from functions, and then returns the modified source code as a string.

##################################################
# TESTS
##################################################

@patch("code_autoeval.clients.llm_model.utils.code_cleaning.auto_function_cleaning.AutoFunctionCleaning.__init__", return_value=None)
def test_normal_case(mock_init):
    # Arrange
    source_code = "def example_func(arg1, arg2):\n    result = arg1 + arg2\n    return result"
    expected_output = "def example_func(arg1):\n    result = arg1 + (lambda _: 0)(0)\n    return result"
    
    # Act
    auto_function_cleaning = AutoFunctionCleaning()
    actual_output = auto_function_cleaning._remove_unused_arguments(source_code)
    
    # Assert
    assert actual_output == expected_output

@patch("code_autoeval.clients.llm_model.utils.code_cleaning.auto_function_cleaning.AutoFunctionCleaning.__init__", return_value=None)
def test_no_unused_args(mock_init):
    # Arrange
    source_code = "def example_func(arg1, arg2):\n    result = arg1 + arg2\n    return result"
    
    # Act
    auto_function_cleaning = AutoFunctionCleaning()
    actual_output = auto_function_cleaning._remove_unused_arguments(source_code)
    
    # Assert
    assert actual_output == source_code

@patch("code_autoeval.clients.llm_model.utils.code_cleaning.auto_function_cleaning.AutoFunctionCleaning.__init__", return_value=None)
def test_empty_source(mock_init):
    # Arrange
    source_code = ""
    
    # Act
    auto_function_cleaning = AutoFunctionCleaning()
    actual_output = auto_function_cleaning._remove_unused_arguments(source_code)
    
    # Assert
    assert actual_output == source_code

@patch("code_autoeval.clients.llm_model.utils.code_cleaning.auto_function_cleaning.AutoFunctionCleaning.__init__", return_value=None)
def test_multiple_functions(mock_init):
    # Arrange
    source_code = """
    def func1(arg1, arg2):
        result = arg1 + arg2
        return result
    
    def func2(arg3, arg4):
        result = arg3 + arg4
        return result
    """
    expected_output = """
    def func1(arg1):
        result = arg1 + (lambda _: 0)(0)
        return result
    
    def func2(arg3, arg4):
        result = arg3 + arg4
        return result
    """
    
    # Act
    auto_function_cleaning = AutoFunctionCleaning()
    actual_output = auto_function_cleaning._remove_unused_arguments(source_code)
    
    # Assert
    assert actual_output == expected_output

@patch("code_autoeval.clients.llm_model.utils.code_cleaning.auto_function_cleaning.AutoFunctionCleaning.__init__", return_value=None)
def test_error_condition(mock_init):
    # Arrange
    source_code = "def example_func(arg1, arg2):\n    result = arg1 + arg2\n    return result"
    
    # Act and Assert
    auto_function_cleaning = AutoFunctionCleaning()
    with pytest.raises(SyntaxError):
        auto_function_cleaning._remove_unused_arguments("invalid source code")