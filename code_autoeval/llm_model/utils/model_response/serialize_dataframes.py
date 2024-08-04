"""Class for serializing dataframes."""

import json
import tempfile
from typing import Optional, Union

import pandas as pd


class SerializeDataframes:
    """Class for serializing dataframes."""

    @staticmethod
    def store_df_in_temp_file(df: Optional[pd.DataFrame] = None) -> str:
        """Store the dataframe in a temporary file."""
        if not isinstance(df, pd.DataFrame) and df is not None:
            raise TypeError("The provided dataframe is not a pandas DataFrame.")

        df_path = ""
        # Create a temporary file to store the dataframe if provided
        if df is not None:
            with tempfile.NamedTemporaryFile(
                mode="wb", suffix=".pkl", delete=False
            ) as temp_df_file:
                df.to_pickle(temp_df_file.name)
                df_path = temp_df_file.name

        return df_path

    def serialize_dataframe(self, df: Union[pd.DataFrame, dict]) -> dict:

        if not isinstance(df, (pd.DataFrame, dict)):
            raise TypeError(
                "The provided data is not a pandas DataFrame or dictionary."
            )

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

        return df

    def deserialize_dataframe(self, obj: dict) -> pd.DataFrame:
        """
        Deserialize a dictionary into a DataFrame.

        :param obj: The dictionary to deserialize.
        :return: The deserialized DataFrame or the input object if not deserializable.
        """
        # Validate that the object is a dictionary and has the correct structure
        if isinstance(obj, dict) and obj.get("type") == "DataFrame":
            try:
                # Deserialize the DataFrame
                df = pd.read_json(json.dumps(obj["data"]), orient="split")

                # Safely parse the dtypes dictionary
                dtypes = json.loads(obj["dtypes"].replace("'", '"'))
                df = df.astype(dtypes)
                return df
            except Exception as e:
                # Handle any exceptions that may occur during deserialization
                print(f"Error during deserialization: {e}")
                return obj

        # Return the original object if it does not match the expected structure
        return obj
