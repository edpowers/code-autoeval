import pytest
from generated_code.fixtures.fixtures.systemprompts_fixture import fixture_mock_systemprompts
from code_autoeval.llm_model.utils.system_prompts import SystemPrompts
def test_mock_systemprompts(fixture_mock_systemprompts):
    assert isinstance(fixture_mock_systemprompts, SystemPrompts)
    assert hasattr(fixture_mock_systemprompts, 'return_analyis_and_guidelines')
    assert isinstance(fixture_mock_systemprompts.return_analyis_and_guidelines, staticmethod)
    assert hasattr(fixture_mock_systemprompts, 'return_example_output')
    assert isinstance(fixture_mock_systemprompts.return_example_output, staticmethod)