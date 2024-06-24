import pandas as pd

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Removes duplicate rows from the given DataFrame.

    If the DataFrame is empty, return an empty DataFrame.
    Make sure the dataframe has an index in the test cases.
    """
    if df.empty:
        return pd.DataFrame()
    
    # Drop duplicates and reset index to ensure the result has a proper index
    cleaned_df = df.drop_duplicates().reset_index(drop=True)
    return cleaned_df