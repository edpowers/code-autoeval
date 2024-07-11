from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.imports.extract_imports_from_file import ExtractImportsFromFile
from pathlib import Path
from typing import Any, Dict
from code_autoeval.llm_model.utils.log_funcs.logging_funcs import LoggingFuncs
from generated_code.fixtures.fixtures.loggingfuncs_fixture import fixture_mock_loggingfuncs
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
@pytest.fixture
def fixture_mock_extractimportsfromfile():
    mock = MagicMock(spec=ExtractImportsFromFile)
    mock.coverage_result = None
    mock.file_path = Path()
    mock.test_file_path = Path()
    mock.absolute_path_from_root = Path()
    mock.unique_imports_dict = {}
    mock._read_in_original_code = MagicMock()
    mock.extract_imports = MagicMock()
    mock.find_original_code_and_imports = classmethod(MagicMock())
    setattr(mock, 'find_original_code_and_imports', classmethod(getattr(mock, 'find_original_code_and_imports').__func__))
    return mock