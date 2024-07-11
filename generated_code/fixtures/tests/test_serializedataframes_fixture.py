import pytest
from generated_code.fixtures.fixtures.serializedataframes_fixture import fixture_mock_serializedataframes
from code_autoeval.llm_model.utils.model_response.serialize_dataframes import SerializeDataframes
def test_mock_serializedataframes(fixture_mock_serializedataframes):
    assert isinstance(fixture_mock_serializedataframes, SerializeDataframes)
    assert hasattr(fixture_mock_serializedataframes, 'deserialize_dataframe')
    assert callable(fixture_mock_serializedataframes.deserialize_dataframe)
    assert hasattr(fixture_mock_serializedataframes, 'serialize_dataframe')
    assert callable(fixture_mock_serializedataframes.serialize_dataframe)
    assert hasattr(fixture_mock_serializedataframes, 'store_df_in_temp_file')
    assert isinstance(fixture_mock_serializedataframes.store_df_in_temp_file, staticmethod)