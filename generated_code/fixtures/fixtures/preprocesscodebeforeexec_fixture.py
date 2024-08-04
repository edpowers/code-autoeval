from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.preprocess_code_before_exec import PreProcessCodeBeforeExec
from pathlib import Path
from typing import Any, Dict, Optional
from code_autoeval.llm_model.utils.validation.validate_regexes import ValidateRegexes
from code_autoeval.llm_model.utils.code_cleaning.run_pyflakes_isort import RunPyflakesIsort
from code_autoeval.llm_model.imports.extract_imports_from_file import ExtractImportsFromFile
from code_autoeval.llm_model.imports.run_flake8_fix_imports import RunFlake8FixImports
from generated_code.fixtures.fixtures.validateregexes_fixture import fixture_mock_validateregexes
from generated_code.fixtures.fixtures.runpyflakesisort_fixture import fixture_mock_runpyflakesisort
from generated_code.fixtures.fixtures.extractimportsfromfile_fixture import fixture_mock_extractimportsfromfile
from generated_code.fixtures.fixtures.runflake8fiximports_fixture import fixture_mock_runflake8fiximports
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
@pytest.fixture
def fixture_mock_preprocesscodebeforeexec():
    mock = MagicMock(spec=PreProcessCodeBeforeExec)
    mock.coverage_result = None
    mock.file_path = Path()
    mock.test_file_path = Path()
    mock.absolute_path_from_root = Path()
    mock.unique_imports_dict = {}
    mock.preprocess_code = MagicMock()
    mock.remove_non_code_patterns = MagicMock()
    mock.run_preprocess_pipeline = MagicMock()
    return mock