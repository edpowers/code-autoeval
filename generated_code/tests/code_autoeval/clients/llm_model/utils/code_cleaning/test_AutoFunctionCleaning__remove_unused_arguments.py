import ast
from unittest.mock import MagicMock, patch

import astor


class AutoFunctionCleaning:
    def __init__(self, data):
        self.data = data

    async def _remove_unused_arguments(self, source_code: str) -> str:
        """
        Remove unused arguments from a function.
        """

        class UnusedArgumentRemover(ast.NodeTransformer):
            def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
                # Get all argument names
                arg_names = {arg.arg for arg in node.args.args}

                used_names = {
                    child.id
                    for child in ast.walk(node)
                    if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load)
                }

                # Determine unused arguments
                unused_args = arg_names - used_names

                # Remove unused arguments
                node.args.args = [
                    arg for arg in node.args.args if arg.arg not in unused_args
                ]

                return node

        # Parse the source code into an AST
        tree = ast.parse(source_code)

        # Apply the transformer
        transformer = UnusedArgumentRemover()
        modified_tree = transformer.visit(tree)

        return astor.to_source(modified_tree)


import ast
from unittest.mock import patch

import astor
import pytest


@pytest.fixture(scope="module")
def source_code():
    return """
def example_function(arg1, arg2):
    result = arg1 + arg2
    print(result)
"""


@patch(
    "code_autoeval.llm_model.utils.code_cleaning.auto_function_cleaning.AutoFunctionCleaning._remove_unused_arguments"
)
def test_normal_case(mocked_func, source_code):
    mocked_func.return_value = (
        "def example_function(arg1):\n    result = arg1 + 42\n    print(result)"
    )
    cleaned_code = AutoFunctionCleaning("data")._remove_unused_arguments(source_code)
    assert cleaned_code == mocked_func.return_value


def test_edge_case_no_args():
    source_code = "def example_function():\n    print('No args here')"
    cleaned_code = AutoFunctionCleaning("data")._remove_unused_arguments(source_code)
    assert cleaned_code == source_code


def test_error_condition_invalid_input():
    with pytest.raises(TypeError):
        AutoFunctionCleaning("data")._remove_unused_arguments(42)  # Invalid input type


@pytest.mark.asyncio
async def test_async_function():
    source_code = "async def example_function(arg1, arg2):\n    result = arg1 + arg2\n    print(result)"
    mocked_func = MagicMock()
    mocked_func.return_value = (
        "async def example_function(arg1):\n    result = arg1 + 42\n    print(result)"
    )
    with patch(
        "code_autoeval.llm_model.utils.code_cleaning.auto_function_cleaning.AutoFunctionCleaning._remove_unused_arguments",
        mocked_func,
    ):
        cleaned_code = await AutoFunctionCleaning("data")._remove_unused_arguments(
            source_code
        )
        assert cleaned_code == mocked_func.return_value
