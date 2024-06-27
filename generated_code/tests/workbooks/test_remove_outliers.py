import pytest
import pandas as pd
from generated_code.workbooks.remove_outliers import remove_outliers

import pytest


def test_normal_case():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5, 100]})
    expected_output = pd.DataFrame({"A": [1, 2, 3, 4, 5]})
    assert remove_outliers(df, "A").equals(expected_output)


def test_non_numerical_column():
    df = pd.DataFrame({"A": ["a", "b", "c"]})
    original_df = df.copy()
    result = remove_outliers(df, "A")
    assert df.equals(result)  # Ensure the original DataFrame is unchanged
    assert remove_outliers(original_df, "A").columns == ["A"]  # Check column name


def test_edge_case_empty_column():
    df = pd.DataFrame({"A": []})
    expected_output = pd.DataFrame({"A": []})
    assert remove_outliers(df, "A").equals(expected_output)


def test_error_condition_non_existent_column():
    df = pd.DataFrame({"A": [1, 2, 3]})
    with pytest.raises(KeyError):
        remove_outliers(df, "B")


def test_edge_case_single_value():
    df = pd.DataFrame({"A": [1]})
    expected_output = pd.DataFrame({"A": [1]})
    assert remove_outliers(df, "A").equals(expected_output)
