from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.extraction.extract_context_from_exception import ExtractContextFromException
@pytest.fixture
def fixture_mock_extractcontextfromexception():
    mock = MagicMock(spec=ExtractContextFromException)
    return mock