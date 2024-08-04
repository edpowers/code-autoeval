from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.code_cleaning.run_pyflakes_isort import RunPyflakesIsort
from pathlib import Path
from typing import Any, Dict, Optional
from code_autoeval.llm_model.utils.log_funcs.logging_funcs import LoggingFuncs
from generated_code.fixtures.fixtures.loggingfuncs_fixture import fixture_mock_loggingfuncs
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
@pytest.fixture(name="fixture_mock_runpyflakesisort")
def fixture_mock_runpyflakesisort():
    mock = MagicMock(spec=RunPyflakesIsort)
    mock.coverage_result = None
    mock.file_path = Path()
    mock.test_file_path = Path()
    mock.absolute_path_from_root = Path()
    mock.unique_imports_dict = {}
    mock.add_class_import = MagicMock()
    mock.parse_pyflakes_output = MagicMock()
    mock.remove_unused_imports = MagicMock()
    mock.run_pyflakes_isort_pipeline = MagicMock()
    return mock
