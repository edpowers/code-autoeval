from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.imports.global_imports import GlobalImports
@pytest.fixture
def fixture_mock_globalimports():
    mock = MagicMock(spec=GlobalImports)
    mock._extract_sys_module_prefix = MagicMock()
    mock._import_libraries = MagicMock()
    mock.create_global_imports = classmethod(MagicMock())
    setattr(mock, 'create_global_imports', classmethod(getattr(mock, 'create_global_imports').__func__))
    mock.find_imports_from_env = MagicMock()
    mock.return_global_vars = MagicMock()
    mock.run_global_imports = MagicMock()
    return mock
