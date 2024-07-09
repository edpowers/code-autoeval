from code_autoeval.llm_model.utils.model_response.serializing_dataframes import SerializeDataframes
from code_autoeval.llm_model.utils.find_parent_class import FindParentClass
from code_autoeval.llm_model.utils.preprocess_code_before_execution import PreProcessCodeBeforeExecution
from code_autoeval.llm_model.utils.validation.validate_regexes import ValidateRegexes
import pytest
from generated_code.fixtures.fixtures.executegeneratedcode_fixture import fixture_mock_executegeneratedcode
from code_autoeval.llm_model.utils.execute_generated_code import ExecuteGeneratedCode
from pathlib import Path
from typing import Any, Dict
def test_mock_executegeneratedcode(fixture_mock_executegeneratedcode):
    assert isinstance(fixture_mock_executegeneratedcode, ExecuteGeneratedCode)
    assert hasattr(fixture_mock_executegeneratedcode, 'execute_generated_code')
    assert callable(fixture_mock_executegeneratedcode.execute_generated_code)
    assert hasattr(fixture_mock_executegeneratedcode, 'extract_imports_from_gen_code')
    assert callable(fixture_mock_executegeneratedcode.extract_imports_from_gen_code)
    assert hasattr(fixture_mock_executegeneratedcode, 'find_args_for_generated_function')
    assert callable(fixture_mock_executegeneratedcode.find_args_for_generated_function)
    assert hasattr(fixture_mock_executegeneratedcode, 'get_imported_libraries')
    assert callable(fixture_mock_executegeneratedcode.get_imported_libraries)
    assert hasattr(fixture_mock_executegeneratedcode, 'import_required_libraries')
    assert callable(fixture_mock_executegeneratedcode.import_required_libraries)
    assert hasattr(fixture_mock_executegeneratedcode, 'coverage_result')
    assert hasattr(fixture_mock_executegeneratedcode, 'file_path')
    assert isinstance(fixture_mock_executegeneratedcode.file_path, Path)
    assert hasattr(fixture_mock_executegeneratedcode, 'test_file_path')
    assert isinstance(fixture_mock_executegeneratedcode.test_file_path, Path)
    assert hasattr(fixture_mock_executegeneratedcode, 'absolute_path_from_root')
    assert isinstance(fixture_mock_executegeneratedcode.absolute_path_from_root, Path)
    assert hasattr(fixture_mock_executegeneratedcode, 'unique_imports_dict')
    assert isinstance(fixture_mock_executegeneratedcode.unique_imports_dict, Dict)
    assert hasattr(fixture_mock_executegeneratedcode, 'imported_libraries')
    assert isinstance(fixture_mock_executegeneratedcode.imported_libraries, set)
    assert isinstance(fixture_mock_executegeneratedcode, SerializeDataframes)
    assert isinstance(fixture_mock_executegeneratedcode, PreProcessCodeBeforeExecution)
    assert isinstance(fixture_mock_executegeneratedcode, FindParentClass)
    assert isinstance(fixture_mock_executegeneratedcode, ValidateRegexes)