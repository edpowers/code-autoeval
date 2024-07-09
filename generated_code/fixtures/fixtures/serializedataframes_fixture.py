from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.model_response.serializing_dataframes import SerializeDataframes
@pytest.fixture
def fixture_mock_serializedataframes():
    mock = MagicMock(spec=SerializeDataframes)
    mock.deserialize_dataframe = MagicMock()
    mock.serialize_dataframe = MagicMock()
    return mock