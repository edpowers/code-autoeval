from code_autoeval.llm_model.utils.prompting.dynamic_example_prompt import DynamicExamplePrompt
from code_autoeval.llm_model.utils.prompting.dynamic_example_prompt import DynamicExamplePrompt
import pytest
from generated_code.fixtures.fixtures.systemprompts_fixture import fixture_mock_systemprompts
from code_autoeval.llm_model.utils.prompting.system_prompts import SystemPrompts
def test_mock_systemprompts(fixture_mock_systemprompts):
    assert isinstance(fixture_mock_systemprompts, SystemPrompts)
    assert hasattr(fixture_mock_systemprompts, 'generate_clarification_prompt')
    assert callable(fixture_mock_systemprompts.generate_clarification_prompt)
    assert hasattr(fixture_mock_systemprompts, 'generate_fake_data_prompt')
    assert callable(fixture_mock_systemprompts.generate_fake_data_prompt)
    assert hasattr(fixture_mock_systemprompts, 'generate_prompt_for_mock_hierarchy')
    assert callable(fixture_mock_systemprompts.generate_prompt_for_mock_hierarchy)
    assert hasattr(fixture_mock_systemprompts, 'generate_system_prompt')
    assert callable(fixture_mock_systemprompts.generate_system_prompt)
    assert hasattr(fixture_mock_systemprompts, 'generate_system_prompt_no_existing_function')
    assert callable(fixture_mock_systemprompts.generate_system_prompt_no_existing_function)
    assert hasattr(fixture_mock_systemprompts, 'generate_system_prompt_with_existing_function')
    assert callable(fixture_mock_systemprompts.generate_system_prompt_with_existing_function)
    assert hasattr(fixture_mock_systemprompts, 'provide_async_or_sync_mocking_structure')
    assert callable(fixture_mock_systemprompts.provide_async_or_sync_mocking_structure)
    assert hasattr(fixture_mock_systemprompts, 'provide_init_mocking_example')
    assert callable(fixture_mock_systemprompts.provide_init_mocking_example)
    assert hasattr(fixture_mock_systemprompts, 'return_analyis_and_guidelines')
    assert isinstance(fixture_mock_systemprompts.return_analyis_and_guidelines, staticmethod)
    assert hasattr(fixture_mock_systemprompts, 'return_example_output')
    assert isinstance(fixture_mock_systemprompts.return_example_output, staticmethod)
    assert isinstance(fixture_mock_systemprompts, DynamicExamplePrompt)