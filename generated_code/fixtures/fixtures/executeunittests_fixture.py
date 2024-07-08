from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.execute_unit_tests import ExecuteUnitTests
from pathlib import Path
from typing import Dict
import subprocess
from code_autoeval.llm_model.utils.preprocess_code_before_execution import PreProcessCodeBeforeExecution
from code_autoeval.llm_model.utils.extraction.parse_unit_test_coverage import ParseUnitTestCoverage
from generated_code.fixtures.fixtures.preprocesscodebeforeexecution_fixture import fixture_mock_preprocesscodebeforeexecution
from generated_code.fixtures.fixtures.parseunittestcoverage_fixture import fixture_mock_parseunittestcoverage
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
@pytest.fixture
def fixture_mock_executeunittests():
    mock = MagicMock(spec=ExecuteUnitTests)
    mock.coverage_result = None
    mock.file_path = Path('/')
    mock.test_file_path = Path('/')
    mock.absolute_path_from_root = Path('/')
    mock.unique_imports_dict = {}
    return mock