import os
import tempfile
from unittest.mock import patch

import pytest

from code_autoeval.llm_model.utils.model.class_data_model import ClassDataModel
from code_autoeval.llm_model.utils.model.function_attributes import FunctionAttributes
from code_autoeval.llm_model.utils.preprocess_code_before_execution import (
    PreProcessCodeBeforeExecution,
)


class TestPreProcessCodeBeforeExecution:
    @patch(
        "code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution._log_code"
    )
    @patch(
        "code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution.extract_imports"
    )
    def test_normal_use_case(self, mock_extract_imports, mock_log_code):
        # Arrange
        code = "print('Hello, World!')"
        max_line_length = 480
        class_model = ClassDataModel()
        func_attributes = FunctionAttributes()
        is_pytest_format = False
        preprocess = PreProcessCodeBeforeExecution()

        # Mock the file reading and imports extraction
        mock_extract_imports.return_value = []
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        # Act
        result, _ = preprocess.preprocess_code(
            code, max_line_length, class_model, func_attributes, is_pytest_format
        )

        # Assert
        assert result == code
        os.unlink(temp_file_path)

    @patch(
        "code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution._log_code"
    )
    @patch(
        "code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution.extract_imports"
    )
    def test_edge_case_empty_code(self, mock_extract_imports, mock_log_code):
        # Arrange
        code = ""
        max_line_length = 480
        class_model = ClassDataModel()
        func_attributes = FunctionAttributes()
        is_pytest_format = False
        preprocess = PreProcessCodeBeforeExecution()

        # Mock the file reading and imports extraction
        mock_extract_imports.return_value = []
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        # Act
        result, _ = preprocess.preprocess_code(
            code, max_line_length, class_model, func_attributes, is_pytest_format
        )

        # Assert
        assert result == code
        os.unlink(temp_file_path)

    @patch(
        "code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution._log_code"
    )
    @patch(
        "code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution.extract_imports"
    )
    def test_error_condition_invalid_file(self, mock_extract_imports, mock_log_code):
        # Arrange
        code = "print('Hello, World!')"
        max_line_length = 480
        class_model = ClassDataModel()
        func_attributes = FunctionAttributes()
        is_pytest_format = False
        preprocess = PreProcessCodeBeforeExecution()

        # Mock the file reading and imports extraction
        mock_extract_imports.return_value = []
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        # Act and Assert
        with pytest.raises(FileNotFoundError):
            preprocess.preprocess_code(
                code, max_line_length, class_model, func_attributes, is_pytest_format
            )

        os.unlink(temp_file_path)

    @patch(
        "code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution._log_code"
    )
    @patch(
        "code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution.extract_imports"
    )
    def test_pytest_format(self, mock_extract_imports, mock_log_code):
        # Arrange
        code = "def test_function(): pass"
        max_line_length = 480
        class_model = ClassDataModel()
        func_attributes = FunctionAttributes()
        is_pytest_format = True
        preprocess = PreProcessCodeBeforeExecution()

        # Mock the file reading and imports extraction
        mock_extract_imports.return_value = []
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        # Act
        result, _ = preprocess.preprocess_code(
            code, max_line_length, class_model, func_attributes, is_pytest_format
        )

        # Assert
        assert result == code
        os.unlink(temp_file_path)

    @patch(
        "code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution._log_code"
    )
    @patch(
        "code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution.extract_imports"
    )
    def test_class_definition(self, mock_extract_imports, mock_log_code):
        # Arrange
        code = "class TestClass: pass"
        max_line_length = 480
        class_model = ClassDataModel()
        func_attributes = FunctionAttributes()
        is_pytest_format = False
        preprocess = PreProcessCodeBeforeExecution()

        # Mock the file reading and imports extraction
        mock_extract_imports.return_value = []
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        # Act and Assert
        with pytest.raises(
            Exception
        ):  # Adjust the exception type based on actual implementation
            preprocess.preprocess_code(
                code, max_line_length, class_model, func_attributes, is_pytest_format
            )

        os.unlink(temp_file_path)  # Act and Assert
        with pytest.raises(
            Exception
        ):  # Adjust the exception type based on actual implementation
            preprocess.preprocess_code(
                code, max_line_length, class_model, func_attributes, is_pytest_format
            )

        os.unlink(temp_file_path)
