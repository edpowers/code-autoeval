# Updated Implementation of PreProcessCodeBeforeExecution._format_code_with_black function
import re
from unittest.mock import patch

import pytest


class PreProcessCodeBeforeExecution:
    def __init__(self):
        pass

    @staticmethod
    def _format_code_with_black(self, code: str, **kwargs) -> str:
        # Then verify that we don't have the class definition in the test file.
        if f"class {kwargs['class_name']}" in code:
            # Remove actual class definition
            code = self.remove_class_definition(code, kwargs['class_name'])

            # Check if there's still a class definition (which might be a patched recreation)
            remaining_class_def = re.search(
                rf"\s*class\s+{re.escape(kwargs['class_name'])}\s*(\([^)]*\))?\s*:", code
            )
            if remaining_class_def:
                # If it's within a patch or mock context, it's okay
                patch_context = re.search(
                    rf"(@patch|mock\.patch|with\s+patch)[^\n]*\n\s*class\s+{re.escape(kwargs['class_name'])}",
                    code,
                )
                if not patch_context:
                    raise ValueError(
                        f"Unexpected class definition for {kwargs['class_name']} found in the pytest tests."
                    )

        if f"class {kwargs['class_name']}" in code:
            raise ValueError(
                f"Class definition for {kwargs['class_name']} found in the pytest tests."
            )

        return code

    @staticmethod
    def remove_class_definition(code: str, class_name: str) -> str:
        # Implement the logic to remove the class definition from the code
        pattern = re.compile(rf"class\s+{re.escape(class_name)}\s*(\([^)]*\))?\s*:")
        return re.sub(pattern, "", code)

##################################################
# TESTS
##################################################

@patch("code_autoeval.clients.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution._format_code_with_black")
def test_normal_use_case(mock_format_code):
    # Arrange
    code = "class TestClass:\n    pass"
    class_name = "TestClass"
    mock_format_code.return_value = code

    # Act
    result = PreProcessCodeBeforeExecution._format_code_with_black(None, code, class_name=class_name)

    # Assert
    assert result == code

def test_edge_case_no_class():
    # Arrange
    code = "print('Hello, World!')"
    class_name = "TestClass"

    # Act & Assert
    with pytest.raises(ValueError):
        PreProcessCodeBeforeExecution._format_code_with_black(None, code, class_name=class_name)

def test_error_condition():
    # Arrange
    code = "class TestClass:\n    pass"
    class_name = "TestClass"

    # Act & Assert
    with pytest.raises(ValueError):
        PreProcessCodeBeforeExecution._format_code_with_black(None, code, class_name=class_name)

def test_mocking():
    # Arrange
    code = "class TestClass:\n    pass"
    class_name = "TestClass"

    with patch("code_autoeval.clients.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution._format_code_with_black") as mock_format_code:
        # Act & Assert
        PreProcessCodeBeforeExecution._format_code_with_black(None, code, class_name=class_name)
        assert mock_format_code.called