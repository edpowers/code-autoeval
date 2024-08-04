from unittest.mock import MagicMock

import pytest
from code_autoeval.llm_model.utils.prompting.system_prompts import SystemPrompts


@pytest.fixture(scope='module')
def mock_systemprompts():
    return SystemPrompts()

def test_SystemPrompts_generate_prompt_for_mock_hierarchy(mock_systemprompts):
    # Arrange
    self = MagicMock()
    class_hierarchy = {
        "ClassA": {"attributes": ["attr1", "attr2"], "methods": ["method1", "method2"]},
        "ClassB": {"attributes": ["attr3", "attr4"], "methods": ["method3", "method4"]}
    }

    instance = mock_systemprompts

    # Act
    result = instance.generate_prompt_for_mock_hierarchy(class_hierarchy)

    # Assert
    assert isinstance(result, str)
    assert "You are an expert Python developer specializing in creating robust testing infrastructures." in result
    assert "Your task is to create a pytest conftest.py file" in result
    assert "Class Hierarchy:" in result
    assert '{"ClassA": {"attributes": ["attr1", "attr2"], "methods": ["method1", "method2"]},' in result
    assert '"ClassB": {"attributes": ["attr3", "attr4"], "methods": ["method3", "method4"]}' in result