import unittest.mock as mock
from pathlib import Path
from typing import Dict, List, Tuple

import pytest
from code_autoeval.clients.llm_model.utils.model.class_data_model import ClassDataModel, ClassDataModelFactory

# Function Analysis:
# The function `create_from_class_info` processes class information to create instances of `ClassDataModel`.
# It iterates over a dictionary containing file paths and lists of tuples with class names, import paths, and function names.
# For each class, it imports the class, retrieves its attributes, methods, etc., and creates a `ClassDataModel` instance.
# The function handles potential errors by printing error messages but continues processing other classes.

def test_create_from_class_info_normal():
    # Arrange
    class_info = {
        "file1.py": [("ClassName1", "path.to.Class", ["method1"])],
        "file2.py": [("ClassName2", "path.to.Class", ["method2"])]
    }
    factory = ClassDataModelFactory()
    factory._import_class = mock.Mock(return_value=None)
    SystemUtils = mock.Mock()
    SystemUtils.get_class_file_path = mock.Mock(return_value="mocked/path")
    
    # Act
    result = factory.create_from_class_info(class_info)
    
    # Assert
    assert len(result) == 2
    assert all(isinstance(item, ClassDataModel) for item in result)

def test_create_from_class_info_no_functions():
    # Arrange
    class_info = {
        "file1.py": [("ClassName1", "path.to.Class", [])]
    }
    factory = ClassDataModelFactory()
    factory._import_class = mock.Mock(return_value=None)
    
    # Act
    result = factory.create_from_class_info(class_info)
    
    # Assert
    assert len(result) == 0

def test_create_from_class_info_error():
    # Arrange
    class_info = {
        "file1.py": [("ClassName1", "non.existent.path", ["method1"])]
    }
    factory = ClassDataModelFactory()
    factory._import_class = mock.Mock(side_effect=Exception("Import error"))
    
    # Act
    result = factory.create_from_class_info(class_info)
    
    # Assert
    assert len(result) == 0

def test_create_from_class_info_mocking():
    # Arrange
    class_info = {
        "file1.py": [("ClassName1", "path.to.Class", ["method1"])]
    }
    factory = ClassDataModelFactory()
    with mock.patch("code_autoeval.clients.llm_model.utils.model.class_data_model.SystemUtils") as SystemUtils_mock:
        SystemUtils_mock.get_class_file_path.return_value = "mocked/path"
        factory._import_class = mock.Mock(return_value=None)
        
    # Act
    result = factory.create_from_class_info(class_info)
    
    # Assert
    assert len(result) == 1
    assert isinstance(result[0], ClassDataModel)

def test_create_from_class_info_empty_input():
    # Arrange
    class_info = {}
    factory = ClassDataModelFactory()
    
    # Act
    result = factory.create_from_class_info(class_info)
    
    # Assert
    assert len(result) == 0