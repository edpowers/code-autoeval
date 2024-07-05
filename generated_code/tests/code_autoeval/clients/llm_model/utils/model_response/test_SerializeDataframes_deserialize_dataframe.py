import json
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest


class SerializeDataframes:
    def deserialize_dataframe(self, obj: dict) -> pd.DataFrame:
        if isinstance(obj, dict) and obj.get("type") == "DataFrame":
            df = pd.read_json(json.dumps(obj["data"]), orient="split")
            df = df.astype(eval(obj["dtypes"]))
            return df
        return obj

# Analysis:
# The function `deserialize_dataframe` is designed to convert a dictionary representation of a DataFrame back into a pandas DataFrame object.
# It checks if the input object is a dictionary and has a "type" key with value "DataFrame". If so, it reads the data from JSON format,
# converts it to a DataFrame, applies the specified dtypes, and returns the DataFrame. Otherwise, it simply returns the original object.

##################################################
# TESTS
##################################################

@patch("code_autoeval.clients.llm_model.utils.model_response.serializing_dataframes.SerializeDataframes")
def test_deserialize_dataframe_normal(mock_serialize):
    mock_instance = mock_serialize.return_value
    obj = {
        "type": "DataFrame",
        "data": {"columns": ["A", "B"], "index": [0, 1], "values": [[1, 2], [3, 4]]},
        "dtypes": "{'A': 'int', 'B': 'int'}"
    }
    expected_df = pd.DataFrame([[1, 2], [3, 4]], columns=["A", "B"])
    expected_df["A"] = expected_df["A"].astype(int)
    expected_df["B"] = expected_df["B"].astype(int)
    
    result = mock_instance.deserialize_dataframe(obj)
    pd.testing.assert_frame_equal(result, expected_df)

def test_deserialize_dataframe_not_dict():
    obj = "not a dict"
    assert SerializeDataframes().deserialize_dataframe(obj) == obj

def test_deserialize_dataframe_wrong_type():
    obj = {"type": "NotDataFrame"}
    result = SerializeDataframes().deserialize_dataframe(obj)
    assert result == obj

def test_deserialize_dataframe_missing_dtypes():
    obj = {
        "type": "DataFrame",
        "data": {"columns": ["A", "B"], "index": [0, 1], "values": [[1, 2], [3, 4]]}
    }
    expected_df = pd.DataFrame([[1, 2], [3, 4]], columns=["A", "B"])
    
    result = SerializeDataframes().deserialize_dataframe(obj)
    pd.testing.assert_frame_equal(result, expected_df)

def test_deserialize_dataframe_missing_data():
    obj = {
        "type": "DataFrame",
        "dtypes": "{'A': 'int', 'B': 'int'}"
    }
    with pytest.raises(KeyError):
        SerializeDataframes().deserialize_dataframe(obj)