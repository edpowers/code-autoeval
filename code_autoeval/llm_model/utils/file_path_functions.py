"""Interactions for file path functions."""

import ast
import os
import re

# Import the base llm class
from code_autoeval.llm_model.utils.base_llm_class import BaseLLMClass

# TODO: Fix these.


class FilePathFunctions(BaseLLMClass):
    """File path functions."""

    def find_function_file(self, func_name: str, base_dir: str) -> str:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        tree = ast.parse(f.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef) and node.name == func_name:
                            return (
                                file_path.replace(base_dir, "")
                                .strip(os.path.sep)
                                .replace(os.path.sep, ".")
                            )
        return None

    def update_import_statement(
        self, code: str, func_name: str, base_dir: str, debug: bool = False
    ) -> str:
        if not (file_path := self.find_function_file(func_name, base_dir)):
            raise FileNotFoundError(f"Function {func_name} not found in {base_dir}")

        module_name = os.path.splitext(file_path)[0]
        new_import = f"from {module_name} import {func_name}"

        if debug:
            print(f"Updating import statement to: {new_import}")

        return re.sub(f"from.*import.*{func_name}", new_import, code)
