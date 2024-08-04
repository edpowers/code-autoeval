from unittest.mock import MagicMock

import pytest
from code_autoeval.llm_model.utils.preprocess_code_before_exec import PreProcessCodeBeforeExec


@pytest.fixture(scope='module')
def mock_preprocesscodebeforeexec():
    return PreProcessCodeBeforeExec()

def test_PreProcessCodeBeforeExec_run_preprocess_pipeline_normal_use_case(mock_preprocesscodebeforeexec):
    # Arrange
    self = MagicMock()
    code = "print('Hello, World!')"
    max_line_length = 120
    class_model = MagicMock()
    func_attributes = MagicMock()
    is_pytest_format = False
    kwargs = {}

    instance = mock_preprocesscodebeforeexec

    # Act
    result = instance.run_preprocess_pipeline(self, code, max_line_length, class_model, func_attributes, is_pytest_format, **kwargs)

    # Assert
    assert isinstance(result, str)
    assert "print('Hello, World!')" in result

def test_PreProcessCodeBeforeExec_run_preprocess_pipeline_edge_case_empty_code(mock_preprocesscodebeforeexec):
    # Arrange
    self = MagicMock()
    code = ""
    max_line_length = 120
    class_model = MagicMock()
    func_attributes = MagicMock()
    is_pytest_format = False
    kwargs = {}

    instance = mock_preprocesscodebeforeexec

    # Act
    result = instance.run_preprocess_pipeline(self, code, max_line_length, class_model, func_attributes, is_pytest_format, **kwargs)

    # Assert
    assert isinstance(result, str)
    assert result == ""

def test_PreProcessCodeBeforeExec_run_preprocess_pipeline_error_case_invalid_code(mock_preprocesscodebeforeexec):
    # Arrange
    self = MagicMock()
    code = "print('Hello, World!"  # Missing closing quote
    max_line_length = 120
    class_model = MagicMock()
    func_attributes = MagicMock()
    is_pytest_format = False
    kwargs = {}

    instance = mock_preprocesscodebeforeexec

    # Act and Assert
    with pytest.raises(SyntaxError):
        result = instance.run_preprocess_pipeline(self, code, max_line_length, class_model, func_attributes, is_pytest_format, **kwargs)