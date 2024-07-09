from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.execute_generated_code import ExecuteGeneratedCode
from pathlib import Path
from typing import Any, Dict
from generated_code.fixtures.fixtures.serializedataframes_fixture import fixture_mock_serializedataframes
from generated_code.fixtures.fixtures.preprocesscodebeforeexecution_fixture import fixture_mock_preprocesscodebeforeexecution
from generated_code.fixtures.fixtures.findparentclass_fixture import fixture_mock_findparentclass
from generated_code.fixtures.fixtures.validateregexes_fixture import fixture_mock_validateregexes
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
@pytest.fixture
def fixture_mock_executegeneratedcode():
    mock = MagicMock(spec=ExecuteGeneratedCode)
    mock.coverage_result = None
    mock.file_path = Path()
    mock.test_file_path = Path()
    mock.absolute_path_from_root = Path()
    mock.unique_imports_dict = {}
    mock.imported_libraries = set()
    mock.execute_generated_code = MagicMock()
    mock.extract_imports_from_gen_code = MagicMock()
    mock.find_args_for_generated_function = MagicMock()
    mock.get_imported_libraries = MagicMock()
    mock.import_required_libraries = MagicMock()
    return mock