"""Finding the parent class."""

import ast
from typing import Tuple

import astor


class FindParentClass:
    """Given a function, find the associated parent class."""

    def update_local_var_names(self, local_vars: dict) -> dict:
        """Update the local variable names to avoid conflicts."""
        # Map local_vars keys to class._func_name if it exists
        updated_local_vars = {}
        for key, value in local_vars.items():
            if isinstance(value, type) and hasattr(value, "_func_name"):
                updated_local_vars[value._func_name] = value
            else:
                updated_local_vars[key] = value

        return updated_local_vars

    def find_target_in_code(self, code: str, target_name: str) -> ast.AST:
        """
        Parse the code and find the target function or class.

        :param code: The code string to parse
        :param target_name: The name of the function or class to find
        :return: The AST node of the target function or class, or None if not found
        """
        tree = ast.parse(code)
        return next(
            (
                node
                for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.ClassDef))
                and (node.name in target_name or target_name in node.name)
            ),
            None,
        )

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
