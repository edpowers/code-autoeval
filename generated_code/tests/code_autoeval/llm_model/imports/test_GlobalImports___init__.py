import pytest
from generated_code.fixtures.fixtures.globalimports_fixture import fixture_mock_globalimports
from typing import Set, Dict, Any
import DEFAULT_GLOBAL_IMPORTS  # Assuming this is a module containing default global imports

# Use the pre-defined fixture to get correctly typed dependencies
@pytest.mark.asyncio
async def test_globalimports_init(fixture_mock_globalimports):
    dependencies = fixture_mock_globalimports()
    
    # Create an instance of the actual class
    instance = GlobalImports(**dependencies.__dict__)
    
    # Test if the initialization parameters are set correctly
    assert isinstance(instance.imported_libraries, Set)
    assert isinstance(instance.default_global_imports, Dict)