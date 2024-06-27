# REMOVED DUE TO PARSING ERROR: Here are the pytest tests for this function:

import pytest
import pandas as pd
import numpy as np


def remove_outliers(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Removes outliers from the given DataFrame column.

    If the column does not contain numerical data, then log the column name - data type,
    and return the original dataframe.

    Numerical column data types can be defined as:
        np.number, np.int64, np.float64, np.float32, np.int32, np.int16, np.float16

    Please use a library that preserves the temporal nature of the data, without
    introducing leakage or bias.
    """
    if not np.issubdtype(df[column].dtype, np.number):
        print(f"Non-numerical column: {column} - {df[column].dtype}")
        return df

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    filtered_df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return filtered_df


# Test the function
print(remove_outliers(pd.DataFrame({"A": [1, 2, 3, 4, 5, 100]}), "A"))
