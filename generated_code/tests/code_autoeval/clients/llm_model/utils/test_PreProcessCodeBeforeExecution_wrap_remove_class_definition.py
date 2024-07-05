from unittest.mock import patch

import pytest


def wrap_remove_class_definition(self, code: str, class_name: str) -> str:
    # Remove leading/trailing whitespace
    code = code.strip()

    # Escape any existing double quotes in the code
    code = code.replace('"', '\\"')

    return f'"""\n{code}\n"""'


##################################################
# TESTS
##################################################


@patch(
    "code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution.wrap_remove_class_definition"
)
def test_normal_use_case(mock_wrap):
    # Arrange
    code = "class MyClass:\n    pass"
    class_name = "MyClass"

    # Act
    result = wrap_remove_class_definition(None, code, class_name)

    # Assert
    mock_wrap.assert_called_once_with(None, code, class_name)
    assert result == '"""\nclass MyClass:\n    pass\n"""'


def test_empty_code():
    # Arrange
    code = ""
    class_name = "MyClass"

    # Act
    result = wrap_remove_class_definition(None, code, class_name)

    # Assert
    assert result == '"""'


def test_code_with_quotes():
    # Arrange
    code = 'class MyClass:\n    print("Hello World")'
    class_name = "MyClass"

    # Act
    result = wrap_remove_class_definition(None, code, class_name)

    # Assert
    assert result == '"""\nclass MyClass:\n    print("Hello World")\n"""'


def test_no_class_definition():
    # Arrange
    code = "print('Hello')"
    class_name = "MyClass"

    # Act
    result = wrap_remove_class_definition(None, code, class_name)

    # Assert
    assert result == '"""\nprint(\'Hello\')\n"""'


def test_error_condition():
    # Arrange
    code = "class MyClass:\n    pass"
    class_name = ""  # Invalid class name, should raise an error

    # Act & Assert
    with pytest.raises(TypeError):
        wrap_remove_class_definition(None, code, class_name)
