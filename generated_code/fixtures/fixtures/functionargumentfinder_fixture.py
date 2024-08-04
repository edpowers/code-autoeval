from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.extraction.function_argument_finder import FunctionArgumentFinder
@pytest.fixture
def fixture_mock_functionargumentfinder():
    mock = MagicMock(spec=FunctionArgumentFinder)
    mock._get_default_for_type = MagicMock()
    mock._log = MagicMock()
    mock._resolve_argument = MagicMock()
    mock.find_args = MagicMock()
    return mock
