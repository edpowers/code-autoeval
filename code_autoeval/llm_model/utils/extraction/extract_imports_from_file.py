"""Auto-extract imports from file."""

import ast
import re
from typing import Dict


class ExtractImportsFromFile:
    """Auto-extract imports from file."""

    def _extract_imports(self, file_content: str) -> Dict[str, str]:
        tree = ast.parse(file_content)
        imports = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports[alias.name] = f"import {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                names = [alias.name for alias in node.names]
                if len(names) == 1:
                    imports[names[0]] = f"from {module} import {names[0]}"
                else:
                    imports[tuple(names)] = f"from {module} import ({', '.join(names)})"

        return imports

    def extract_imports(self, file_content: str) -> Dict[str, str]:
        imports = {}

        # Remove comments
        file_content = re.sub(r"#.*$", "", file_content, flags=re.MULTILINE)

        # Find all import statements, including multi-line ones
        import_statements = re.findall(
            r"^(?:from .+? import [^(]+?|\s*import .+?)(?:\n|$)|\([\s\S]+?\)",
            file_content,
            re.MULTILINE,
        )

        for statement in import_statements:
            statement = statement.strip()
            if statement.startswith("from"):
                # Handle 'from ... import ...' statements
                module, names = statement.split(" import ", 1)
                names = re.split(r",\s*", names.strip("()"))
                for name in names:
                    name = name.strip()
                    if " as " in name:
                        name = name.split(" as ")[1]
                    imports[name] = (
                        statement.replace("\n", " ").replace("(", "").replace(")", "")
                    )
            elif statement.startswith("import"):
                # Handle 'import ...' statements
                names = statement.split("import ")[1]
                for name in re.split(r",\s*", names):
                    name = name.strip()
                    if " as " in name:
                        name = name.split(" as ")[1]
                    imports[name] = statement

        return imports
