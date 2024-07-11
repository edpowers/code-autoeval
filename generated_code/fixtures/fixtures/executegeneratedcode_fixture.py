from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.execute_generated_code import ExecuteGeneratedCode
from pathlib import Path
from typing import Any, Dict
from code_autoeval.llm_model.utils.model_response.serialize_dataframes import SerializeDataframes
from code_autoeval.llm_model.utils.preprocess_code_before_exec import PreProcessCodeBeforeExec
from code_autoeval.llm_model.utils.extraction.find_parent_class import FindParentClass
from code_autoeval.llm_model.utils.validation.validate_regexes import ValidateRegexes
from code_autoeval.llm_model.imports.extract_imports_from_file import ExtractImportsFromFile
from code_autoeval.llm_model.imports.dynamically_import_packages import DynamicallyImportPackages
from generated_code.fixtures.fixtures.serializedataframes_fixture import fixture_mock_serializedataframes
from generated_code.fixtures.fixtures.preprocesscodebeforeexec_fixture import fixture_mock_preprocesscodebeforeexec
from generated_code.fixtures.fixtures.findparentclass_fixture import fixture_mock_findparentclass
from generated_code.fixtures.fixtures.validateregexes_fixture import fixture_mock_validateregexes
from generated_code.fixtures.fixtures.extractimportsfromfile_fixture import fixture_mock_extractimportsfromfile
from generated_code.fixtures.fixtures.dynamicallyimportpackages_fixture import fixture_mock_dynamicallyimportpackages
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.functionargumentfinder_fixture import fixture_mock_functionargumentfinder
from generated_code.fixtures.fixtures.globalimports_fixture import fixture_mock_globalimports
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
@pytest.fixture
def fixture_mock_executegeneratedcode():
    mock = MagicMock(spec=ExecuteGeneratedCode)
    mock.coverage_result = None
    mock.file_path = Path("/")
    mock.test_file_path = Path("/")
    mock.absolute_path_from_root = Path("/")
    mock.unique_imports_dict = {}
    mock.imported_libraries = set()
    mock.execute_generated_code = MagicMock()
    return mock