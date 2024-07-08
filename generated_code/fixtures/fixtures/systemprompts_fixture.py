from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.system_prompts import SystemPrompts
@pytest.fixture(name="fixture_mock_systemprompts")
def fixture_mock_systemprompts():
    mock = MagicMock(spec=SystemPrompts)
    mock.return_analyis_and_guidelines = None
    mock.return_example_output = None
    return mock