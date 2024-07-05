from unittest.mock import patch

import pytest


# Assuming ValidateRegexes is a class defined in code_autoeval.llm_model.utils.validation.validate_regexes
class ValidateRegexes:
    def validate_class_name_in_local_vars(self, class_name: str, local_vars: dict) -> None:
        """Validate that the parent name class is in the local vars."""
        if class_name not in local_vars:
            raise ValueError(f"Parent class name '{class_name}' not found in the local vars.")

from unittest.mock import patch

import pytest


@pytest.mark.parametrize("class_name, local_vars", [
    ("ParentClass", {"ParentClass": object}),
    ("AnotherClass", {"AnotherClass": int})
])
def test_normal_case(class_name, local_vars):
    with patch("code_autoeval.llm_model.utils.validation.validate_regexes.ValidateRegexes") as mock_validate:
        instance = mock_validate.return_value
        instance.validate_class_name_in_local_vars(class_name, local_vars)
        assert True  # No exception means the test passes

def test_missing_class():
    class_name = "MissingClass"
    local_vars = {"ExistingClass": object}
    with pytest.raises(ValueError):
        with patch("code_autoeval.llm_model.utils.validation.validate_regexes.ValidateRegexes") as mock_validate:
            instance = mock_validate.return_value
            instance.validate_class_name_in_local_vars(class_name, local_vars)

def test_empty_local_vars():
    class_name = "ClassInEmptyLocalVars"
    local_vars = {}
    with pytest.raises(ValueError):
        with patch("code_autoeval.llm_model.utils.validation.validate_regexes.ValidateRegexes") as mock_validate:
            instance = mock_validate.return_value
            instance.validate_class_name_in_local_vars(class_name, local_vars)    with pytest.raises(ValueError):
        with patch("code_autoeval.llm_model.utils.validation.validate_regexes.ValidateRegexes") as mock_validate:
            instance = mock_validate.return_value
            instance.validate_class_name_in_local_vars(class_name, local_vars)