import re
from typing import Tuple

from code_autoeval.llm_model.utils.model.class_data_model import ClassDataModel


class RunPyflakesIsort:
    def __init__(self, data):
        self.data = data

    async def add_class_import(self, code: str, class_model: 'ClassDataModel') -> Tuple[str, bool]:
        """Add import for the class if it's not."""
        absolute_path = class_model.absolute_path.rsplit(".", maxsplit=1)[0]
        new_import_line = f"from {absolute_path} import {class_model.class_name}\n"

        lines = code.splitlines()
        new_lines = []
        was_modified = False

        for line in lines:
            if re.search(rf"\bimport\s+{class_model.class_name}\b", line) or re.search(
                rf"\bfrom\s+.*\s+import\s+.*\b{class_model.class_name}\b", line
            ):
                was_modified = True
                continue
            new_lines.append(line)

        if new_import_line.strip() not in [line.strip() for line in new_lines]:
            import_index = next(
                (
                    i
                    for i, line in enumerate(new_lines)
                    if line.startswith("import") or line.startswith("from")
                ),
                0,
            )
            new_lines.insert(import_index, new_import_line.strip())
            was_modified = True

        return "\n".join(new_lines), was_modified

from unittest.mock import patch

import pytest

from code_autoeval.llm_model.utils.code_cleaning.run_pyflakes_isort import \
    RunPyflakesIsort


@pytest.fixture
def class_model():
    return type('ClassDataModel', (object,), {'absolute_path': 'module.Class', 'class_name': 'Class'})

@pytest.fixture
def initial_code():
    return "existing code\nimport another_class"

async def test_add_class_import_normal(initial_code, class_model):
    run_pyflakes = RunPyflakesIsort(None)
    new_code, modified = await run_pyflakes.add_class_import(initial_code, class_model)
    assert "from module import Class" in new_code
    assert modified is True

async def test_add_class_import_already_exists(initial_code, class_model):
    initial_code += "\nfrom module import Class"
    run_pyflakes = RunPyflakesIsort(None)
    new_code, modified = await run_pyflakes.add_class_import(initial_code, class_model)
    assert "from module import Class" in new_code
    assert modified is False

async def test_add_class_import_no_existing_imports(initial_code, class_model):
    initial_code = "existing code without imports"
    run_pyflakes = RunPyflakesIsort(None)
    new_code, modified = await run_pyflakes.add_class_import(initial_code, class_model)
    assert "from module import Class" in new_code
    assert modified is True

async def test_add_class_import_empty_code():
    initial_code = ""
    class_model = type('ClassDataModel', (object,), {'absolute_path': 'module.Class', 'class_name': 'Class'})
    run_pyflakes = RunPyflakesIsort(None)
    new_code, modified = await run_pyflakes.add_class_import(initial_code, class_model)
    assert "from module import Class" in new_code
    assert modified is True

async def test_add_class_import_no_modification():
    initial_code = "existing code\nfrom another_module import AnotherClass"
    class_model = type('ClassDataModel', (object,), {'absolute_path': 'another_module.AnotherClass', 'class_name': 'AnotherClass'})
    run_pyflakes = RunPyflakesIsort(None)
    new_code, modified = await run_pyflakes.add_class_import(initial_code, class_model)
    assert "from another_module import AnotherClass" in new_code
    assert modified is False    new_code, modified = await run_pyflakes.add_class_import(initial_code, class_model)
    assert "from another_module import AnotherClass" in new_code
    assert modified is False