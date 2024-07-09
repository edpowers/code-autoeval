from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.base_llm_class import InitKwargs
@pytest.fixture
def fixture_mock_initkwargs():
    mock = MagicMock(spec=InitKwargs)
    mock.verbose = False
    mock.debug = False
    mock.func_name = ""
    return mock
