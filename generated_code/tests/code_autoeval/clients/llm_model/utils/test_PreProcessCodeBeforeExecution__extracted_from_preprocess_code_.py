import subprocess
from typing import Dict, Optional, Tuple
from unittest.mock import MagicMock, patch

import pytest
from code_autoeval.llm_model.utils.model.class_data_model import ClassDataModel


class PreProcessCodeBeforeExecution:
    def __init__(self):
        self.unique_imports_dict = {}  # Example of class attribute initialization

    async def _extracted_from_preprocess_code_(self, temp_file_path, code, max_line_length, class_model=None, original_imports=None):
        was_modified = False

        flake8_result = subprocess.run(
            ["flake8", "--select=E999,F401,F821,F822,F823,F841,E501", temp_file_path],
            capture_output=True,
            text=True,
        )

        problematic_lines, undefined_names = self.parse_flake8_output(flake8_result)

        import_lines_to_add = []

        if class_model and class_model.class_name in undefined_names:
            absolute_path = class_model.absolute_path.rsplit(".", maxsplit=1)[0]
            import_line_to_add = f"from {absolute_path} import {class_model.class_name}"
            import_lines_to_add.append(import_line_to_add)
            undefined_names.remove(class_model.class_name)

        import_lines_to_add.extend(
            original_imports[name] for name in undefined_names if name in original_imports
        )

        remaining_undefined = undefined_names - set(name for name in import_lines_to_add)

        for name in list(remaining_undefined):
            if name in self.unique_imports_dict:
                import_lines_to_add.append(self.unique_imports_dict[name])
                remaining_undefined.remove(name)
            if name in {"MagicMock", "patch", "AsyncMock"}:
                import_lines_to_add.append(f"from unittest.mock import {name}")
                remaining_undefined.remove(name)
            if name in {"tmp_path", "capsys", "caplog"}:
                import_lines_to_add.append(f"from pytest import {name}")
                remaining_undefined.remove(name)

        if remaining_undefined:
            raise ImportError(f"Unresolved import errors for: {', '.join(remaining_undefined)}")

        if problematic_lines:
            self._log_code(str(problematic_lines), "Problematic lines:")

        lines = code.splitlines()

        if import_lines_to_add:
            processed_lines = import_lines_to_add + lines
            was_modified = True
        else:
            processed_lines = lines

        return "\n".join(processed_lines), was_modified

    def parse_flake8_output(self, flake8_result):
        # Mock implementation for parsing flake8 output
        problematic_lines = []
        undefined_names = set()
        return problematic_lines, undefined_names

    def _log_code(self, code, message):
        print(f"{message}\n{code}")

import subprocess
from typing import Dict, Optional, Tuple
from unittest.mock import MagicMock, patch

import pytest
from code_autoeval.llm_model.utils.model.class_data_model import ClassDataModel


class PreProcessCodeBeforeExecution:
    def __init__(self):
        self.unique_imports_dict = {}  # Example of class attribute initialization

    async def _extracted_from_preprocess_code_(self, temp_file_path, code, max_line_length, class_model=None, original_imports=None):
        was_modified = False

        flake8_result = subprocess.run(
            ["flake8", "--select=E999,F401,F821,F822,F823,F841,E501", temp_file_path],
            capture_output=True,
            text=True,
        )

        problematic_lines, undefined_names = self.parse_flake8_output(flake8_result)

        import_lines_to_add = []

        if class_model and class_model.class_name in undefined_names:
            absolute_path = class_model.absolute_path.rsplit(".", maxsplit=1)[0]
            import_line_to_add = f"from {absolute_path} import {class_model.class_name}"
            import_lines_to_add.append(import_line_to_add)
            undefined_names.remove(class_model.class_name)

        import_lines_to_add.extend(
            original_imports[name] for name in undefined_names if name in original_imports
        )

        remaining_undefined = undefined_names - set(name for name in import_lines_to_add)

        for name in list(remaining_undefined):
            if name in self.unique_imports_dict:
                import_lines_to_add.append(self.unique_imports_dict[name])
                remaining_undefined.remove(name)
            if name in {"MagicMock", "patch", "AsyncMock"}:
                import_lines_to_add.append(f"from unittest.mock import {name}")
                remaining_undefined.remove(name)
            if name in {"tmp_path", "capsys", "caplog"}:
                import_lines_to_add.append(f"from pytest import {name}")
                remaining_undefined.remove(name)

        if remaining_undefined:
            raise ImportError(f"Unresolved import errors for: {', '.join(remaining_undefined)}")

        if problematic_lines:
            self._log_code(str(problematic_lines), "Problematic lines:")

        lines = code.splitlines()

        if import_lines_to_add:
            processed_lines = import_lines_to_add + lines
            was_modified = True
        else:
            processed_lines = lines

        return "\n".join(processed_lines), was_modified

    def parse_flake8_output(self, flake8_result):
        # Mock implementation for parsing flake8 output
        problematic_lines = []
        undefined_names = set()
        return problematic_lines, undefined_names

    def _log_code(self, code, message):
        print(f"{message}\n{code}")

##################################################
# TESTS
##################################################

@pytest.mark.asyncio
async def test_normal_case():
    preprocessor = PreProcessCodeBeforeExecution()
    temp_file_path = "test_file.py"
    code = "print('Hello, World!')"
    max_line_length = 80
    class_model = None
    original_imports = {}

    result, modified = await preprocessor._extracted_from_preprocess_code_(temp_file_path, code, max_line_length, class_model, original_imports)

    assert "print('Hello, World!')" in result
    assert not modified

@pytest.mark.asyncio
async def test_with_undefined_names():
    preprocessor = PreProcessCodeBeforeExecution()
    temp_file_path = "test_file.py"
    code = "some_undefined_function()"
    max_line_length = 80
    class_model = None
    original_imports = {}

    with patch("code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution.parse_flake8_output", return_value=([], {"some_undefined_function"})):
        result, modified = await preprocessor._extracted_from_preprocess_code_(temp_file_path, code, max_line_length, class_model, original_imports)

    assert "from unittest.mock import MagicMock" in result
    assert modified

@pytest.mark.asyncio
async def test_with_problematic_lines():
    preprocessor = PreProcessCodeBeforeExecution()
    temp_file_path = "test_file.py"
    code = "print('A' * 120)"
    max_line_length = 80
    class_model = None
    original_imports = {}

    with patch("code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution._log_code", return_value=None):
        result, modified = await preprocessor._extracted_from_preprocess_code_(temp_file_path, code, max_line_length, class_model, original_imports)

    assert "Problematic lines:" in result
    assert modified

@pytest.mark.asyncio
async def test_with_class_model():
    preprocessor = PreProcessCodeBeforeExecution()
    temp_file_path = "test_file.py"
    code = ""
    max_line_length = 80
    class_model = ClassDataModel("module", "Class")
    original_imports = {}

    with patch("code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution.parse_flake8_output", return_value=([], {"Class"})):
        result, modified = await preprocessor._extracted_from_preprocess_code_(temp_file_path, code, max_line_length, class_model, original_imports)

    assert "from module import Class" in result
    assert modified

@pytest.mark.asyncio
async def test_with_import_errors():
    preprocessor = PreProcessCodeBeforeExecution()
    temp_file_path = "test_file.py"
    code = ""
    max_line_length = 80
    class_model = None
    original_imports = {}

    with patch("code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution.parse_flake8_output", return_value=([], {"NonExistentClass"}), pytest.raises(ImportError)):
        await preprocessor._extracted_from_preprocess_code_(temp_file_path, code, max_line_length, class_model, original_imports)