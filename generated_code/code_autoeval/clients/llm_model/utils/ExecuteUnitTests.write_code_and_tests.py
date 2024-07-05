from unittest.mock import MagicMock, patch

import pytest

from code_autoeval.llm_model.utils.execute_unit_tests import ExecuteUnitTests
from code_autoeval.llm_model.utils.model.class_data_model import ClassDataModel
from code_autoeval.llm_model.utils.model.function_attributes import \
    FunctionAttributes


# Mocking dependencies for the function
@patch("code_autoeval.llm_model.llm_model.LLMModel.__init__", return_value=None)
def test_write_code_and_tests(mock_init):
    # Create an instance of ExecuteUnitTests with mock data
    execute_unit_tests = ExecuteUnitTests()
    execute_unit_tests.validate_test_in_pytest_code = MagicMock()
    execute_unit_tests.run_preprocess_pipeline = MagicMock(return_value="processed_code")
    execute_unit_tests._construct_file_path_and_test_path = MagicMock(return_value=("file_path", "test_file_path", "absolute_path"))
    execute_unit_tests._log_code = MagicMock()

    # Mock data for the function arguments
    code = "def example_func(): return 'Hello, World!'"
    pytest_tests = "def test_example_func(): assert example_func() == 'Hello, World!'"
    func = lambda: None  # Example function
    class_model = ClassDataModel()
    func_attributes = FunctionAttributes(is_coroutine=False)

    # Call the method under test
    execute_unit_tests.write_code_and_tests(code, pytest_tests, func, class_model, func_attributes)

    # Assertions to verify the function's behavior
    assert execute_unit_tests.validate_test_in_pytest_code.called
    assert execute_unit_tests.run_preprocess_pipeline.call_count == 2
    assert execute_unit_tests._construct_file_path_and_test_path.called
    assert execute_unit_tests._log_code.called

    # Check if the code and tests are written to files correctly
    with open("file_path", "r") as f:
        assert f.read() == "def example_func(): return 'Hello, World!'"
    with open("test_file_path", "r") as f:
        assert f.read() == "def test_example_func(): assert example_func() == 'Hello, World!'"        assert f.read() == "def example_func(): return 'Hello, World!'"
    with open("test_file_path", "r") as f:
        assert f.read() == "def test_example_func(): assert example_func() == 'Hello, World!'"