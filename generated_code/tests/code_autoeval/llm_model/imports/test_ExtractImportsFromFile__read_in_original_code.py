from unittest.mock import MagicMock

import pytest
from code_autoeval.llm_model.imports.extract_imports_from_file import ExtractImportsFromFile


@pytest.fixture(scope='module')
def mock_extractimportsfromfile():
    return ExtractImportsFromFile()

def test_ExtractImportsFromFile__read_in_original_code_normal_use_case(mock_extractimportsfromfile):
    # Arrange
    self = MagicMock()
    func_or_class_model = MagicMock()
    func_or_class_model.module_absolute_path = 'test/path/to/module.py'
    func_or_class_model.module_relative_path = 'test.path.to.module'
    
    mock_extractimportsfromfile._log_code = MagicMock()
    
    expected_original_code = "print('Hello, World!')"
    with open(func_or_class_model.module_absolute_path, 'r') as file:
        original_code = file.read()
    
    func_or_class_model.__dict__['original_code'] = expected_original_code

    instance = mock_extractimportsfromfile

    # Act
    result = instance._read_in_original_code(func_or_class_model)

    # Assert
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] == expected_original_code
    assert result[1] == func_or_class_model.module_relative_path.replace('/', '.') + '.py'
    mock_extractimportsfromfile._log_code.assert_called()

def test_ExtractImportsFromFile__read_in_original_code_edge_case(mock_extractimportsfromfile):
    # Arrange
    self = MagicMock()
    func_or_class_model = MagicMock()
    func_or_class_model.module_absolute_path = 'non/existent/path.py'
    
    instance = mock_extractimportsfromfile

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        instance._read_in_original_code(func_or_class_model)

def test_ExtractImportsFromFile__read_in_original_code_error_condition(mock_extractimportsfromfile):
    # Arrange
    self = MagicMock()
    func_or_class_model = MagicMock()
    func_or_class_model.module_absolute_path = ''  # Invalid path
    
    instance = mock_extractimportsfromfile

    # Act & Assert
    with pytest.raises(ValueError):
        instance._read_in_original_code(func_or_class_model)