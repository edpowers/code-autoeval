"""Automatically 'clean' up functions."""

import ast
from typing import List

import astor

from code_autoeval.llm_model.utils.log_funcs import logging_funcs


class FileCleaner(ast.NodeTransformer):
    def __init__(self, cleaner: "AutoFunctionCleaning"):
        self.cleaner = cleaner

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        # Extract the function's source code
        func_source = astor.to_source(node)
        # Clean the function
        cleaned_func_source = self.cleaner._remove_unused_arguments(func_source)
        return ast.parse(cleaned_func_source).body[0]


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
        node.args.args = [arg for arg in node.args.args if arg.arg not in unused_args]

        return node


class AutoFunctionCleaning(logging_funcs.LoggingFuncs):

    def clean_func_args_from_lines(self, code_lines: List[str]) -> List[str]:
        # Join the lines into a single string
        full_code = "\n".join(code_lines)

        # Clean the code
        cleaned_code = self.clean_func_args_from_file(full_code)

        # Split the cleaned code back into lines
        return cleaned_code.split("\n")

    def clean_func_args_from_file(self, file_content: str) -> str:
        """Clean a file by removing unused arguments from functions."""
        # Parse the entire file content into an AST
        tree = ast.parse(file_content)

        # Apply the FileCleaner transformer
        cleaner = FileCleaner(self)
        modified_tree = cleaner.visit(tree)

        return astor.to_source(modified_tree)

    def _remove_unused_arguments(self, source_code: str) -> str:
        """Remove unused arguments from a function."""
        # Parse the source code into an AST
        tree = ast.parse(source_code)

        # Apply the transformer
        transformer = UnusedArgumentRemover()
        modified_tree = transformer.visit(tree)

        return astor.to_source(modified_tree)
