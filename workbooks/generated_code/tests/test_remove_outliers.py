import pytest
import pandas as pd
from generated_code.remove_outliers import remove_outliers

import pytest


def test_remove_outliers_numerical():
    data = {'values': [1, 2, 3, 4, 5, 100]}
    df = pd.DataFrame(data)
    result = remove_outliers(df, 'values')
    expected = pd.DataFrame({'values': [1, 2, 3, 4, 5]})
    pd.testing.assert_frame_equal(result, expected)

def test_remove_outliers_non_numerical():
    data = {'values': ['a', 'b', 'c']}
    df = pd.DataFrame(data)
    result = remove_outliers(df, 'values')
    assert df.equals(result)

def test_remove_outliers_empty_column():
    data = {'values': []}
    df = pd.DataFrame(data)
    result = remove_outliers(df, 'values')
    expected = pd.DataFrame({'values': []})
    pd.testing.assert_frame_equal(result, expected)

def test_remove_outliers_all_same_value():
    data = {'values': [5, 5, 5, 5]}
    df = pd.DataFrame(data)
    result = remove_outliers(df, 'values')
    expected = pd.DataFrame({'values': [5, 5, 5, 5]})
    pd.testing.assert_frame_equal(result, expected)