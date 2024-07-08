from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.code_cleaning.run_flake8_fix_imports import RunFlake8FixImports
@pytest.fixture
def fixture_mock_runflake8fiximports():
    mock = MagicMock(spec=RunFlake8FixImports)
    mock.run_flake8_pipeline_with_temp_file = None
    mock.run_flake_fix_imports = None
    return mock