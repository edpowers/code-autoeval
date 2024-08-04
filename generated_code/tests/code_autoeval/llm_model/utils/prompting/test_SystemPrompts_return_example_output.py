from unittest.mock import MagicMock

import pytest
from code_autoeval.llm_model.utils.prompting.system_prompts import SystemPrompts


@pytest.fixture(scope='module')
def mock_systemprompts():
    return SystemPrompts()

## def test_SystemPrompts.return_example_output(mock_systemprompts):
    # Arrange
    create_function = False
    create_pytests = True
    is_async = True

    instance = mock_systemprompts

    # Act
    result = instance.return_example_output(create_function, create_pytests, is_async)

    # Assert
    assert isinstance(result, str)
    assert "import pytest" in result
    assert "import asyncio" in result
    assert "class TestExampleAsyncFunc:" in result
    assert "assert await example_async_func(3, 4) == 7" in result