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

        # Regular expression to match import statements
        import_pattern = re.compile(
            r"^(from .+? import .+?|\s*import .+?)($|\n)", re.MULTILINE | re.DOTALL
        )

        # Find all matches
        for match in import_pattern.finditer(file_content):
            import_statement = match.group(1).strip()

            # Handle multi-line imports
            if "(" in import_statement and ")" not in import_statement:
                end_index = file_content.index(")", match.end())
                import_statement = file_content[match.start() : end_index + 1].strip()

            # Extract the imported name(s)
            if import_statement.startswith("from"):
                module, names = import_statement.split(" import ")
                names = names.strip("()")
                for name in names.split(","):
                    name = name.strip()
                    if " as " in name:
                        name = name.split(" as ")[1]
                    imports[name] = import_statement
            else:
                names = import_statement.split("import ")[1]
                for name in names.split(","):
                    name = name.strip()
                    if " as " in name:
                        name = name.split(" as ")[1]
                    imports[name] = import_statement

        return imports
