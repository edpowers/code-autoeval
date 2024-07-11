from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.llm_model import LLMModel
from pathlib import Path
from typing import Any, Dict
from code_autoeval.llm_model.utils.execute_generated_code import ExecuteGeneratedCode
from code_autoeval.llm_model.utils.execute_unit_tests import ExecuteUnitTests
from code_autoeval.llm_model.utils.extraction.extract_context_from_exception import ExtractContextFromException
from code_autoeval.llm_model.utils.generate_fake_data import GenerateFakeData
from generated_code.fixtures.fixtures.executegeneratedcode_fixture import fixture_mock_executegeneratedcode
from generated_code.fixtures.fixtures.executeunittests_fixture import fixture_mock_executeunittests
from generated_code.fixtures.fixtures.extractcontextfromexception_fixture import fixture_mock_extractcontextfromexception
from generated_code.fixtures.fixtures.generatefakedata_fixture import fixture_mock_generatefakedata
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.functionargumentfinder_fixture import fixture_mock_functionargumentfinder
from generated_code.fixtures.fixtures.globalimports_fixture import fixture_mock_globalimports
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
@pytest.fixture
def fixture_mock_llmmodel():
    mock = MagicMock(spec=LLMModel)
    mock.coverage_result = None
    mock.file_path = Path()
    mock.test_file_path = Path()
    mock.absolute_path_from_root = Path()
    mock.unique_imports_dict = {}
    mock.imported_libraries = set()
    mock.code_generator = MagicMock()
    return mock
