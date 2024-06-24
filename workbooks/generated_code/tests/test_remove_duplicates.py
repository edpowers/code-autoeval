import pytest
import pandas as pd
from generated_code.remove_duplicates import remove_duplicates

import pytest

#     A  B
# 0  1  a
# 1  2  b
# 2  3  c
# 3  4  d
# 4  5  e
# 5  6  f

import pytest

@pytest.fixture
def df_example():
    data = {
        'A': [1, 2, 3, 4, 5, 6],
        'B': ['a', 'b', 'c', 'd', 'e', 'f']
    }
    return pd.DataFrame(data)

def test_remove_duplicates_basic(df_example):
    result = remove_duplicates(df_example)
    assert result.equals(df_example)

def test_remove_duplicates_empty(df_example):
    empty_df = df_example.iloc[:0]  # Create an empty DataFrame with the same columns
    result = remove_duplicates(empty_df)
    assert result.empty

def test_remove_duplicates_all_duplicates(df_example):
    duplicated_df = pd.concat([df_example, df_example], ignore_index=True)
    result = remove_duplicates(duplicated_df)
    expected = df_example
    assert result.equals(expected)

def test_remove_duplicates_with_index():
    data = {
        'A': [1, 2, 3, 4, 5, 6],
        'B': ['a', 'b', 'c', 'd', 'e', 'f']
    }
    df_example = pd.DataFrame(data)
    result = remove_duplicates(df_example)
    assert isinstance(result.index, pd.RangeIndex)