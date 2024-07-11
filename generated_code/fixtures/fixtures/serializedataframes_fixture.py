from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.model_response.serialize_dataframes import SerializeDataframes
@pytest.fixture
def fixture_mock_serializedataframes():
    mock = MagicMock(spec=SerializeDataframes)
    mock.deserialize_dataframe = MagicMock()
    mock.serialize_dataframe = MagicMock()
    mock.store_df_in_temp_file = staticmethod(MagicMock())
    return mock
