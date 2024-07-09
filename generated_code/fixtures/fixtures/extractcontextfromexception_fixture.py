from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.extraction.extract_context_from_exception import ExtractContextFromException
@pytest.fixture
def fixture_mock_extractcontextfromexception():
    mock = MagicMock(spec=ExtractContextFromException)
    mock._get_relevant_code = MagicMock()
    mock.create_llm_error_prompt = MagicMock()
    mock.format_error = MagicMock()
    return mock
