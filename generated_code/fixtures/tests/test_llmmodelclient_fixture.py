from code_autoeval.llm_model.utils.generate_fake_data import GenerateFakeData
from code_autoeval.llm_model.utils.execute_unit_tests import ExecuteUnitTests
from code_autoeval.llm_model.utils.execute_generated_code import ExecuteGeneratedCode
from code_autoeval.llm_model.utils.extraction.extract_context_from_exception import ExtractContextFromException
import pytest
from generated_code.fixtures.fixtures.llmmodelclient_fixture import fixture_mock_llmmodelclient
from code_autoeval.llm_model.llm_model_client import LLMModelClient
from pathlib import Path
from typing import Any, Dict, Optional
def test_mock_llmmodelclient(fixture_mock_llmmodelclient):
    assert isinstance(fixture_mock_llmmodelclient, LLMModelClient)
    assert hasattr(fixture_mock_llmmodelclient, 'code_generator')
    assert callable(fixture_mock_llmmodelclient.code_generator)
    assert hasattr(fixture_mock_llmmodelclient, 'coverage_result')
    assert hasattr(fixture_mock_llmmodelclient, 'file_path')
    assert isinstance(fixture_mock_llmmodelclient.file_path, Path)
    assert hasattr(fixture_mock_llmmodelclient, 'test_file_path')
    assert isinstance(fixture_mock_llmmodelclient.test_file_path, Path)
    assert hasattr(fixture_mock_llmmodelclient, 'absolute_path_from_root')
    assert isinstance(fixture_mock_llmmodelclient.absolute_path_from_root, Path)
    assert hasattr(fixture_mock_llmmodelclient, 'unique_imports_dict')
    assert isinstance(fixture_mock_llmmodelclient.unique_imports_dict, Dict)
    assert hasattr(fixture_mock_llmmodelclient, 'imported_libraries')
    assert isinstance(fixture_mock_llmmodelclient.imported_libraries, set)
    assert hasattr(fixture_mock_llmmodelclient, 'error_message')
    assert isinstance(fixture_mock_llmmodelclient.error_message, str)
    assert hasattr(fixture_mock_llmmodelclient, 'formatted_error')
    assert isinstance(fixture_mock_llmmodelclient.formatted_error, str)
    assert isinstance(fixture_mock_llmmodelclient, ExecuteGeneratedCode)
    assert isinstance(fixture_mock_llmmodelclient, ExecuteUnitTests)
    assert isinstance(fixture_mock_llmmodelclient, ExtractContextFromException)
    assert isinstance(fixture_mock_llmmodelclient, GenerateFakeData)