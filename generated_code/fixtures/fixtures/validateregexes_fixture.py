from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.validation.validate_regexes import ValidateRegexes
@pytest.fixture
def fixture_mock_validateregexes():
    mock = MagicMock(spec=ValidateRegexes)
    return mock