# Analysis of the function:
# The function `_import_class` is designed to import a specific class from a given module path. 
# It splits the provided import path into module and class names, then uses Python's built-in `importlib` module to dynamically import the specified class.

import pytest
import importlib
from unittest.mock import patch

def _import_class(import_path: str):
    module_name, class_name = import_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

##################################################
# TESTS
##################################################

@patch("importlib.import_module")
def test_normal_use_case(mock_import_module):
    # Arrange
    mock_module = type('MockModule', (object,), {'Class': 'MockClass'})()
    mock_import_module.return_value = mock_module
    
    import_path = "test_module.TestClass"
    
    # Act
    result = _import_class(import_path)
    
    # Assert
    assert result == 'MockClass'
    mock_import_module.assert_called_once_with("test_module")

@patch("importlib.import_module")
def test_invalid_import_path(mock_import_module):
    # Arrange
    mock_import_module.side_effect = ImportError("Mocked Import Error")
    
    import_path = "nonexistent_module.NonExistentClass"
    
    # Act & Assert
    with pytest.raises(ImportError) as excinfo:
        _import_class(import_path)
    assert str(excinfo.value) == "Mocked Import Error"

@patch("importlib.import_module")
def test_missing_class(mock_import_module):
    # Arrange
    mock_module = type('MockModule', (object,), {})()
    mock_import_module.return_value = mock_module
    
    import_path = "test_module.NonExistentClass"
    
    # Act & Assert
    with pytest.raises(AttributeError):
        _import_class(import_path)

@patch("importlib.import_module")
def test_empty_import_path(mock_import_module):
    # Arrange
    import_path = ""
    
    # Act & Assert
    with pytest.raises(ValueError):
        _import_class(import_path)

@patch("importlib.import_module")
def test_none_import_path(mock_import_module):
    # Arrange
    import_path = None
    
    # Act & Assert
    with pytest.raises(TypeError):
        _import_class(import_path)