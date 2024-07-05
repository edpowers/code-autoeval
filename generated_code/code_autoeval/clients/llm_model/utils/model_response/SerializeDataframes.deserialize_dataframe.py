from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

from code_autoeval.llm_model.utils.model_response.serializing_dataframes import \
    SerializeDataframes


class TestSerializeDataframes:
    def test_deserialize_dataframe_normal(self):
        # Arrange
        obj = {
            "type": "DataFrame",
            "data": {"columns": ["A", "B"], "index": [0, 1], "values": [[1, 2], [3, 4]]},
            "dtypes": "{'A': 'int', 'B': 'int'}"
        }
        expected_df = pd.DataFrame({"A": [1, 3], "B": [2, 4]}, index=[0, 1])
        expected_df = expected_df.astype({"A": "int", "B": "int"})

        # Act
        with patch("code_autoeval.llm_model.utils.model_response.serializing_dataframes.pd.read_json") as mock_read_json, \
             patch("code_autoeval.llm_model.utils.model_response.serializing_dataframes.pd.DataFrame.astype") as mock_astype:
            mock_read_json.return_value = expected_df
            mock_astype.return_value = expected_df
            result_df = SerializeDataframes().deserialize_dataframe(obj)

        # Assert
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_deserialize_dataframe_invalid_type(self):
        # Arrange
        obj = {"type": "InvalidType", "data": {}, "dtypes": ""}

        # Act
        result_df = SerializeDataframes().deserialize_dataframe(obj)

        # Assert
        assert result_df == obj

    def test_deserialize_dataframe_missing_keys(self):
        # Arrange
        obj = {"type": "DataFrame", "data": {}, "dtypes": ""}

        # Act
        result_df = SerializeDataframes().deserialize_dataframe(obj)

        # Assert
        assert result_df == obj

    def test_deserialize_dataframe_empty_data(self):
        # Arrange
        obj = {
            "type": "DataFrame",
            "data": {"columns": [], "index": [], "values": []},
            "dtypes": ""
        }
        expected_df = pd.DataFrame(columns=[])

        # Act
        with patch("code_autoeval.llm_model.utils.model_response.serializing_dataframes.pd.read_json") as mock_read_json, \
             patch("code_autoeval.llm_model.utils.model_response.serializing_dataframes.pd.DataFrame.astype") as mock_astype:
            mock_read_json.return_value = expected_df
            mock_astype.return_value = expected_df
            result_df = SerializeDataframes().deserialize_dataframe(obj)

        # Assert
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_deserialize_dataframe_invalid_dtypes(self):
        # Arrange
        obj = {
            "type": "DataFrame",
            "data": {"columns": ["A", "B"], "index": [0, 1], "values": [[1, 2], [3, 4]]},
            "dtypes": "{'A': 'int', 'B': 'str'}"
        }
        expected_df = pd.DataFrame({"A": [1, 3], "B": ["2", "4"]}, index=[0, 1])

        # Act
        with patch("code_autoeval.llm_model.utils.model_response.serializing_dataframes.pd.read_json") as mock_read_json, \
             patch("code_autoeval.llm_model.utils.model_response.serializing_dataframes.pd.DataFrame.astype") as mock_astype:
            mock_read_json.return_value = expected_df
            mock_astype.return_value = expected_df
            result_df = SerializeDataframes().deserialize_dataframe(obj)

        # Assert
        pd.testing.assert_frame_equal(result_df, expected_df)            mock_astype.return_value = expected_df
            result_df = SerializeDataframes().deserialize_dataframe(obj)

        # Assert
        pd.testing.assert_frame_equal(result_df, expected_df)