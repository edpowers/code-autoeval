from code_autoeval.llm_model.utils.execute_unit_tests import ExecuteUnitTests
from code_autoeval.llm_model.utils.extraction.extract_context_from_exception import ExtractContextFromException
from code_autoeval.llm_model.utils.generate_fake_data import GenerateFakeData
from code_autoeval.llm_model.utils.execute_generated_code import ExecuteGeneratedCode
import pytest
from generated_code.fixtures.fixtures.llmmodel_fixture import fixture_mock_llmmodel
from code_autoeval.llm_model.llm_model import LLMModel
from pathlib import Path
from typing import Any, Dict
def test_mock_llmmodel(fixture_mock_llmmodel):
    assert isinstance(fixture_mock_llmmodel, LLMModel)
    assert hasattr(fixture_mock_llmmodel, 'code_generator')
    assert callable(fixture_mock_llmmodel.code_generator)
    assert hasattr(fixture_mock_llmmodel, 'coverage_result')
    assert hasattr(fixture_mock_llmmodel, 'file_path')
    assert isinstance(fixture_mock_llmmodel.file_path, Path)
    assert hasattr(fixture_mock_llmmodel, 'test_file_path')
    assert isinstance(fixture_mock_llmmodel.test_file_path, Path)
    assert hasattr(fixture_mock_llmmodel, 'absolute_path_from_root')
    assert isinstance(fixture_mock_llmmodel.absolute_path_from_root, Path)
    assert hasattr(fixture_mock_llmmodel, 'unique_imports_dict')
    assert isinstance(fixture_mock_llmmodel.unique_imports_dict, Dict)
    assert hasattr(fixture_mock_llmmodel, 'imported_libraries')
    assert isinstance(fixture_mock_llmmodel.imported_libraries, set)
    assert isinstance(fixture_mock_llmmodel, ExecuteGeneratedCode)
    assert isinstance(fixture_mock_llmmodel, ExecuteUnitTests)
    assert isinstance(fixture_mock_llmmodel, ExtractContextFromException)
    assert isinstance(fixture_mock_llmmodel, GenerateFakeData)