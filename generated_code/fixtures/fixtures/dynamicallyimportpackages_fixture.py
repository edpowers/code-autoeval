from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.imports.dynamically_import_packages import DynamicallyImportPackages
from pathlib import Path
from typing import Any, Dict, Set
from code_autoeval.llm_model.utils.log_funcs.logging_funcs import LoggingFuncs
from generated_code.fixtures.fixtures.loggingfuncs_fixture import fixture_mock_loggingfuncs
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
@pytest.fixture
def fixture_mock_dynamicallyimportpackages():
    mock = MagicMock(spec=DynamicallyImportPackages)
    mock.coverage_result = None
    mock.file_path = Path()
    mock.test_file_path = Path()
    mock.absolute_path_from_root = Path()
    mock.unique_imports_dict = {}
    mock.imported_libraries = set()
    mock._extract_libraries = MagicMock()
    mock._import_libraries = MagicMock()
    mock._import_required_libraries = MagicMock()
    mock._parse_flake8_output = MagicMock()
    mock._run_flake8 = MagicMock()
    mock.import_required_libraries = classmethod(MagicMock())
    setattr(mock, 'import_required_libraries', classmethod(getattr(mock, 'import_required_libraries').__func__))
    return mock
