import json
from typing import Union

import pandas as pd


class SerializeDataframes:
    def serialize_dataframe(self, df: Union[pd.DataFrame, dict]) -> dict:
        if isinstance(df, pd.DataFrame):
            if len(df) <= 15:
                sample = df
            else:
                first_5 = df.head(5)
                last_5 = df.tail(5)
                middle_5 = df.iloc[5:-5].sample(5)
                sample = pd.concat([first_5, middle_5, last_5])

            return {
                "type": "DataFrame",
                "data": json.loads(sample.to_json(orient="split")),
                "dtypes": str(df.dtypes.to_dict()),
            }
        elif isinstance(df, dict):
            # Assuming the dictionary represents a DataFrame in JSON format
            return df
        else:
            raise ValueError("Input must be a pandas DataFrame or a dictionary.")

from unittest.mock import patch

import pandas as pd
import pytest
from code_autoeval.clients.llm_model.utils.model_response.serializing_dataframes import SerializeDataframes


# Test the normal use case with a DataFrame
def test_serialize_dataframe_normal():
    df = pd.DataFrame({
        'A': range(1, 20),
        'B': range(20, 40)
    })
    expected_output = {
        "type": "DataFrame",
        "data": json.loads(df.head(5).to_json(orient="split")),
        "dtypes": str({'A': 'int64', 'B': 'int64'})
    }
    result = SerializeDataframes().serialize_dataframe(df)
    assert result == expected_output

# Test the edge case with a small DataFrame
def test_serialize_dataframe_small():
    df = pd.DataFrame({
        'A': range(1, 6),
        'B': range(20, 25)
    })
    expected_output = {
        "type": "DataFrame",
        "data": json.loads(df.to_json(orient="split")),
        "dtypes": str({'A': 'int64', 'B': 'int64'})
    }
    result = SerializeDataframes().serialize_dataframe(df)
    assert result == expected_output

# Test the case with an invalid input (non-DataFrame or non-dict object)
def test_serialize_dataframe_invalid_input():
    with pytest.raises(ValueError):
        SerializeDataframes().serialize_dataframe("not a DataFrame")

# Test the case with a large DataFrame
@patch('code_autoeval.clients.llm_model.utils.model_response.serializing_dataframes.SerializeDataframes._sample_large_df')
def test_serialize_dataframe_large(mock_sample):
    df = pd.DataFrame({
        'A': range(1, 30),
        'B': range(20, 50)
    })
    mock_sample.return_value = df.head(5).append(df.tail(5)).sample(5)
    expected_output = {
        "type": "DataFrame",
        "data": json.loads(mock_sample.return_value.to_json(orient="split")),
        "dtypes": str({'A': 'int64', 'B': 'int64'})
    }
    result = SerializeDataframes().serialize_dataframe(df)
    assert result == expected_output

# Test the case with a dictionary input
def test_serialize_dataframe_dict():
    df_dict = {
        "type": "DataFrame",
        "data": json.dumps({'A': [1, 2, 3], 'B': [4, 5, 6]}),
        "dtypes": "{'A': 'int64', 'B': 'int64'}"
    }
    result = SerializeDataframes().serialize_dataframe(df_dict)
    assert result == df_dict