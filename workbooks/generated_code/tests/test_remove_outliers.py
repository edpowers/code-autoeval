import pytest
import pandas as pd
from generated_code.remove_outliers import remove_outliers

import pytest


def test_remove_outliers_numerical():
    data = {'A': [1, 2, 3, 4, 5, 100]}
    df = pd.DataFrame(data)
    result = remove_outliers(df, 'A')
    expected = pd.DataFrame({'A': [1, 2, 3, 4, 5]})
    pd.testing.assert_frame_equal(result, expected)

def test_remove_outliers_non_numerical():
    data = {'B': ['a', 'b', 'c']}
    df = pd.DataFrame(data)
    result = remove_outliers(df, 'B')
    assert df.equals(result)

def test_remove_outliers_empty_column():
    data = {'C': []}
    df = pd.DataFrame(data)
    result = remove_outliers(df, 'C')
    expected = pd.DataFrame({'C': []})
    pd.testing.assert_frame_equal(result, expected)

def test_remove_outliers_large_values():
    data = {'D': [1, 2, 3, 4, 5, 1000]}
    df = pd.DataFrame(data)
    result = remove_outliers(df, 'D')
    expected = pd.DataFrame({'D': [1, 2, 3, 4, 5]})
    pd.testing.assert_frame_equal(result, expected)