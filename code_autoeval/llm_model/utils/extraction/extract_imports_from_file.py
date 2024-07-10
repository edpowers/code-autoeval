"""Auto-extract imports from file."""

import ast
from typing import Dict, Tuple, Union

from multiuse.model import class_data_model

from code_autoeval.llm_model.utils.logging_statements.logging_statements import (
    LoggingStatements,
)
from code_autoeval.llm_model.utils.model import function_attributes


class ExtractImportsFromFile(LoggingStatements):
    """Auto-extract imports from file."""

    @classmethod
    def find_original_code_and_imports(
        cls,
        func_or_class_model: Union[
            function_attributes.FunctionAttributes, class_data_model.ClassDataModel
        ],
    ) -> Tuple[str, dict]:
        self = cls()
        original_code, relative_fpath = self._read_in_original_code(func_or_class_model)
        original_imports = self.extract_imports(original_code, relative_fpath)
        return original_code, original_imports

    def _read_in_original_code(
        self,
        func_or_class_model: Union[
            function_attributes.FunctionAttributes, class_data_model.ClassDataModel
        ],
    ) -> Tuple[str, str]:
        with open(func_or_class_model.module_absolute_path, "r") as file:
            original_code = file.read()

        self._log_code(
            str(func_or_class_model.module_absolute_path), "Original code file path:"
        )
        self._log_code(original_code, "Original code:")

        relative_fpath = (
            str(func_or_class_model.module_relative_path)
            .replace("/", ".")
            .removesuffix(".py")
        )

        return original_code, relative_fpath

    def extract_imports(
        self,
        file_content: str,
        relative_fpath: str,
    ) -> Dict[str, str]:
        def format_import(module: str, name: str, alias: str = None) -> str:
            if alias and alias != name:
                return f"from {module} import {name} as {alias}"
            return f"from {module} import {name}"

        imports_and_classes = {}
        tree = ast.parse(file_content)
        # Extract __all__ content
        all_names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        if isinstance(node.value, ast.List):
                            all_names = [
                                elt.s
                                for elt in node.value.elts
                                if isinstance(elt, ast.Str)
                            ]

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports_and_classes[alias.asname or alias.name] = (
                        f"import {alias.name}"
                    )
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    name = alias.name
                    asname = alias.asname
                    import_str = format_import(module, name, asname)
                    imports_and_classes[asname or name] = import_str
            elif isinstance(node, ast.ClassDef):
                imports_and_classes[node.name] = format_import(
                    relative_fpath, node.name
                )

        # Add import statements for classes in __all__ that weren't found in the file
        for name in all_names:
            if name not in imports_and_classes:
                imports_and_classes[name] = format_import(relative_fpath, name)

        return imports_and_classes
