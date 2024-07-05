from pathlib import Path
from typing import Dict, List, Tuple
from unittest.mock import MagicMock, patch

import pytest

from code_autoeval.llm_model.utils.model.class_data_model import (
    ClassDataModel,
    ClassDataModelFactory,
)


def test_create_from_class_info():
    # Arrange
    class_info = {
        "file1.py": [("ClassName1", "module.ClassName1", ["method1", "method2"])],
        "file2.py": [("ClassName2", "module.ClassName2", ["method3"])],
    }
    factory = ClassDataModelFactory()
    factory.project_root = Path("/path/to/project")

    # Mock dependencies
    mock_class1 = MagicMock()
    mock_class1.__name__ = "ClassName1"
    mock_class2 = MagicMock()
    mock_class2.__name__ = "ClassName2"

    with patch(
        "code_autoeval.llm_model.utils.model.class_data_model.ClassDataModelFactory._import_class",
        side_effect=[mock_class1, mock_class2],
    ):
        with patch(
            "code_autoeval.llm_model.utils.model.class_data_model.SystemUtils.get_class_file_path",
            return_value="/path/to/module",
        ):
            # Act
            result = factory.create_from_class_info(class_info)

            # Assert
            assert len(result) == 2
            assert all(isinstance(model, ClassDataModel) for model in result)
            assert result[0].class_name == "ClassName1"
            assert result[1].class_name == "ClassName2"


def test_create_from_class_info_no_functions():
    # Arrange
    class_info = {"file1.py": [("ClassName1", "module.ClassName1", [])]}
    factory = ClassDataModelFactory()
    factory.project_root = Path("/path/to/project")

    # Mock dependencies
    mock_class1 = MagicMock()
    mock_class1.__name__ = "ClassName1"

    with patch(
        "code_autoeval.llm_model.utils.model.class_data_model.ClassDataModelFactory._import_class",
        return_value=mock_class1,
    ):
        # Act
        result = factory.create_from_class_info(class_info)

        # Assert
        assert len(result) == 0


def test_create_from_class_info_error():
    # Arrange
    class_info = {
        "file1.py": [
            ("ClassName1", "module.ClassName1", ["method1"]),
            ("ErrorClass", "module.ErrorClass", ["method2"]),
        ]
    }
    factory = ClassDataModelFactory()
    factory.project_root = Path("/path/to/project")

    # Mock dependencies
    mock_class1 = MagicMock()
    mock_class1.__name__ = "ClassName1"
    error_mock = MagicMock(side_effect=Exception("Test Error"))

    with patch(
        "code_autoeval.llm_model.utils.model.class_data_model.ClassDataModelFactory._import_class",
        return_value=mock_class1,
    ):
        with patch(
            "code_autoeval.llm_model.utils.model.class_data_model.SystemUtils.get_class_file_path",
            return_value="/path/to/module",
        ):
            with patch(
                "code_autoeval.llm_model.utils.model.class_data_model.ClassDataModelFactory._get_base_classes",
                side_effect=error_mock,
            ):
                # Act
                result = factory.create_from_class_info(class_info)

                # Assert
                assert len(result) == 1
                assert result[0].class_name == "ClassName1"


def test_create_from_class_info_no_classes():
    # Arrange
    class_info = {}
    factory = ClassDataModelFactory()
    factory.project_root = Path("/path/to/project")

    # Act
    result = factory.create_from_class_info(class_info)

    # Assert
    assert len(result) == 0


def test_create_from_class_info_mocked():
    # Arrange
    class_info = {"file1.py": [("ClassName1", "module.ClassName1", ["method1"])]}
    factory = ClassDataModelFactory()
    factory.project_root = Path("/path/to/project")

    # Mock dependencies
    mock_class1 = MagicMock()
    mock_class1.__name__ = "ClassName1"

    with patch(
        "code_autoeval.llm_model.utils.model.class_data_model.ClassDataModelFactory._import_class",
        return_value=mock_class1,
    ):
        with patch(
            "code_autoeval.llm_model.utils.model.class_data_model.SystemUtils.get_class_file_path",
            return_value="/path/to/module",
        ):
            # Act
            result = factory.create_from_class_info(class_info)

            # Assert
            assert len(result) == 1
            assert result[0].class_name == "ClassName1"  # Act
            result = factory.create_from_class_info(class_info)

            # Assert
            assert len(result) == 1
            assert result[0].class_name == "ClassName1"
