from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.system_prompts import SystemPrompts
@pytest.fixture
def fixture_mock_systemprompts():
    mock = MagicMock(spec=SystemPrompts)
    mock._return_example_output = staticmethod(MagicMock())
    mock.generate_clarification_prompt = MagicMock()
    mock.generate_fake_data_prompt = MagicMock()
    mock.generate_prompt_for_mock_hierarchy = MagicMock()
    mock.generate_system_prompt = MagicMock()
    mock.generate_system_prompt_no_existing_function = MagicMock()
    mock.generate_system_prompt_with_existing_function = MagicMock()
    mock.provide_async_or_sync_mocking_structure = MagicMock()
    mock.provide_init_mocking_example = MagicMock()
    mock.return_analyis_and_guidelines = staticmethod(MagicMock())
    mock.return_example_output = staticmethod(MagicMock())
    return mock