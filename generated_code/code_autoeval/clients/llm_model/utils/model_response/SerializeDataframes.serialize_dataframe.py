import pytest
import pandas as pd
from unittest.mock import patch, PropertyMock

class SerializeDataframes:
    def serialize_dataframe(self, df):
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
                "data": sample.to_json(orient="split"),
                "dtypes": str(df.dtypes.to_dict()),
            }
        return df

# Updated implementation of the SerializeDataframes.serialize_dataframe function.

##################################################
# TESTS
##################################################

@pytest.mark.asyncio
async def test_serialize_dataframe():
    # Arrange
    ser = SerializeDataframes()
    
    # Create a mock DataFrame with 20 rows and 5 columns
    data = {f'col{i}': list(range(1, 21)) for i in range(1, 6)}
    mock_df = pd.DataFrame(data)
    
    # Act
    result = await ser.serialize_dataframe(mock_df)
    
    # Assert
    assert result["type"] == "DataFrame"
    assert isinstance(result["data"], str)
    assert result["dtypes"] == "{'col1': 'int64', 'col2': 'int64', 'col3': 'int64', 'col4': 'int64', 'col5': 'int64'}"

@pytest.mark.asyncio
async def test_serialize_small_dataframe():
    # Arrange
    ser = SerializeDataframes()
    
    # Create a mock DataFrame with 10 rows and 3 columns
    data = {f'col{i}': list(range(1, 11)) for i in range(1, 4)}
    mock_df = pd.DataFrame(data)
    
    # Act
    result = await ser.serialize_dataframe(mock_df)
    
    # Assert
    assert result == mock_df

@pytest.mark.asyncio
async def test_serialize_large_dataframe():
    # Arrange
    ser = SerializeDataframes()
    
    # Create a mock DataFrame with 25 rows and 3 columns
    data = {f'col{i}': list(range(1, 26)) for i in range(1, 4)}
    mock_df = pd.DataFrame(data)
    
    # Act
    result = await ser.serialize_dataframe(mock_df)
    
    # Assert
    assert result["type"] == "DataFrame"
    assert isinstance(result["data"], str)
    assert result["dtypes"] == "{'col1': 'int64', 'col2': 'int64', 'col3': 'int64'}"

@pytest.mark.asyncio
async def test_serialize_empty_dataframe():
    # Arrange
    ser = SerializeDataframes()
    
    # Create an empty DataFrame
    mock_df = pd.DataFrame()
    
    # Act
    result = await ser.serialize_dataframe(mock_df)
    
    # Assert
    assert result == mock_df

@pytest.mark.asyncio
async def test_serialize_non_dataframe():
    # Arrange
    ser = SerializeDataframes()
    
    # Pass a non-DataFrame object
    mock_dict = {"key": "value"}
    
    # Act
    result = await ser.serialize_dataframe(mock_dict)
    
    # Assert
    assert result == mock_dict

@pytest.mark.asyncio
async def test_serialize_nan_values():
    # Arrange
    ser = SerializeDataframes()
    
    # Create a DataFrame with NaN values
    data = {f'col{i}': [float('nan')] * 20 for i in range(1, 6)}
    mock_df = pd.DataFrame(data)
    
    # Act
    result = await ser.serialize_dataframe(mock_df)
    
    # Assert
    assert result["type"] == "DataFrame"
    assert isinstance(result["data"], str)
    assert result["dtypes"] == "{'col1': 'float64', 'col2': 'float64', 'col3': 'float64', 'col4': 'float64', 'col5': 'float64'}"

@pytest.mark.asyncio
async def test_serialize_large_nan_dataframe():
    # Arrange
    ser = SerializeDataframes()
    
    # Create a DataFrame with NaN values and more than 15 rows
    data = {f'col{i}': [float('nan')] * 25 for i in range(1, 4)}
    mock_df = pd.DataFrame(data)
    
    # Act
    result = await ser.serialize_dataframe(mock_df)
    
    # Assert
    assert result["type"] == "DataFrame"
    assert isinstance(result["data"], str)
    assert result["dtypes"] == "{'col1': 'float64', 'col2': 'float64', 'col3': 'float64'}"