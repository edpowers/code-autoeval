import pytest
from generated_code.fixtures.fixtures.globalimports_fixture import fixture_mock_globalimports
from code_autoeval.llm_model.imports.global_imports import GlobalImports
def test_mock_globalimports(fixture_mock_globalimports):
    assert isinstance(fixture_mock_globalimports, GlobalImports)
    assert hasattr(fixture_mock_globalimports, '_extract_sys_module_prefix')
    assert callable(fixture_mock_globalimports._extract_sys_module_prefix)
    assert hasattr(fixture_mock_globalimports, '_import_libraries')
    assert callable(fixture_mock_globalimports._import_libraries)
    assert hasattr(fixture_mock_globalimports, 'create_global_imports')
    assert isinstance(fixture_mock_globalimports.create_global_imports, classmethod)
    assert callable(fixture_mock_globalimports.create_global_imports.__func__)
    assert hasattr(fixture_mock_globalimports, 'find_imports_from_env')
    assert callable(fixture_mock_globalimports.find_imports_from_env)
    assert hasattr(fixture_mock_globalimports, 'return_global_vars')
    assert callable(fixture_mock_globalimports.return_global_vars)
    assert hasattr(fixture_mock_globalimports, 'run_global_imports')
    assert callable(fixture_mock_globalimports.run_global_imports)
    assert hasattr(fixture_mock_globalimports, 'create_global_imports')
    assert isinstance(fixture_mock_globalimports.create_global_imports, classmethod)