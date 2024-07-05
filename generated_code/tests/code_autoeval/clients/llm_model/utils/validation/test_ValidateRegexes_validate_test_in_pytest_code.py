from unittest.mock import patch

import pytest


class ValidateRegexes:
    def __init__(self, *args, **kwargs):
        pass

    async def validate_test_in_pytest_code(self, pytest_code: str) -> None:
        if "def test_" not in pytest_code:
            raise ValueError(f"pytest_tests must be in {pytest_code}")

##################################################
# TESTS
##################################################

@patch("code_autoeval.clients.llm_model.utils.validation.validate_regexes.ValidateRegexes.__init__", return_value=None)
def test_normal_case(mock_init):
    # Arrange
    validate = ValidateRegexes()
    pytest_code = "def test_example(): pass"
    
    # Act & Assert
    assert validate.validate_test_in_pytest_code(pytest_code) is None

@patch("code_autoeval.clients.llm_model.utils.validation.validate_regexes.ValidateRegexes.__init__", return_value=None)
def test_missing_test_definition(mock_init):
    # Arrange
    validate = ValidateRegexes()
    pytest_code = "def some_other_function(): pass"
    
    # Act & Assert
    with pytest.raises(ValueError):
        validate.validate_test_in_pytest_code(pytest_code)

@patch("code_autoeval.clients.llm_model.utils.validation.validate_regexes.ValidateRegexes.__init__", return_value=None)
def test_empty_string(mock_init):
    # Arrange
    validate = ValidateRegexes()
    pytest_code = ""
    
    # Act & Assert
    with pytest.raises(ValueError):
        validate.validate_test_in_pytest_code(pytest_code)

@patch("code_autoeval.clients.llm_model.utils.validation.validate_regexes.ValidateRegexes.__init__", return_value=None)
def test_none_input(mock_init):
    # Arrange
    validate = ValidateRegexes()
    pytest_code = None
    
    # Act & Assert
    with pytest.raises(ValueError):
        validate.validate_test_in_pytest_code(pytest_code)

@patch("code_autoeval.clients.llm_model.utils.validation.validate_regexes.ValidateRegexes.__init__", return_value=None)
def test_whitespace_input(mock_init):
    # Arrange
    validate = ValidateRegexes()
    pytest_code = "   "
    
    # Act & Assert
    with pytest.raises(ValueError):
        validate.validate_test_in_pytest_code(pytest_code)