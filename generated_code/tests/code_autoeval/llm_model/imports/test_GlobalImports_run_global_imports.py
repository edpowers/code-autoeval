## :
## ```python
from unittest.mock import MagicMock

import pytest
from code_autoeval.llm_model.imports.global_imports import GlobalImports


@pytest.fixture(scope='module')
def mock_globalimports():
    return GlobalImports()

def test_GlobalImports_run_global_imports_normal_use_case(mock_globalimports):
    # Arrange
    instance = mock_globalimports
    
    # Act
    result = instance.run_global_imports()
    
    # Assert
    assert isinstance(result, dict)
    assert 'imported_libraries' in result
    imported_libs = result['imported_libraries']
    assert len(imported_libs) == 2
    for lib in ['lib1', 'lib2']:
        assert lib in globals()

def test_GlobalImports_run_global_imports_edge_case_no_default_imports(mock_globalimports):
    # Arrange
    instance = mock_globalimports
    instance.default_global_imports = {}
    
    # Act
    result = instance.run_global_imports()
    
    # Assert
    assert isinstance(result, dict)
    assert 'imported_libraries' in result
    imported_libs = result['imported_libraries']
    assert len(imported_libs) == 0

def test_GlobalImports_run_global_imports_error_case_invalid_library(mock_globalimports):
    # Arrange
    instance = mock_globalimports
    with pytest.raises(ImportError):
        instance._import_libraries({'invalid_lib'})
    
    # Act & Assert are combined in the context manager above

def test_GlobalImports_run_global_imports_performance_case_large_number_of_imports(mock_globalimports):
    # Arrange
    instance = mock_globalimports
    large_set = set('lib' + str(i) for i in range(1000))
    
    # Act
    result = instance._import_libraries(large_set)
    
    # Assert
    assert len(globals()) == 1001  # Including the original globals from the fixture setup