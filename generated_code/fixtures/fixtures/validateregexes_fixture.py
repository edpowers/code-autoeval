from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.validation.validate_regexes import ValidateRegexes
@pytest.fixture
def fixture_mock_validateregexes():
    mock = MagicMock(spec=ValidateRegexes)
    mock.validate_class_name_in_local_vars = MagicMock()
    mock.validate_func_in_code = MagicMock()
    mock.validate_func_name_in_code = MagicMock()
    mock.validate_target_node = MagicMock()
    mock.validate_test_in_pytest_code = MagicMock()
    return mock
