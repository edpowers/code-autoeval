from unittest.mock import MagicMock

import pytest
from code_autoeval.llm_model.utils.prompting.system_prompts import SystemPrompts


@pytest.fixture(scope='module')
def mock_systemprompts():
    return SystemPrompts()

def test_SystemPrompts_provide_init_mocking_example(mock_systemprompts):
    # Arrange
    self = MagicMock()
    class_name = "SystemPrompts"
    class_relative_path = "/path/to/SystemPrompts.py"
    fixture_import_statement = 'from generated_code.fixtures.fixtures.systemprompts_fixture import fixture_mock_systemprompts'
    init_params = ['args', 'kwargs']
    class_attributes = []
    base_classes = ['DynamicExamplePrompt']

    instance = mock_systemprompts

    # Act
    result = instance.provide_init_mocking_example(self, class_name, class_relative_path, fixture_import_statement, init_params, class_attributes, base_classes)

    # Assert
    assert isinstance(result, str)
    assert "To test the SystemPrompts class initialization" in result
    assert f"def test_{class_name.lower()}_init({fixture_import_statement.split(' import ')[-1].strip()}):" in result