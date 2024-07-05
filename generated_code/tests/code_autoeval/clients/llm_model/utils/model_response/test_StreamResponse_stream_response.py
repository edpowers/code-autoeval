# Updated Implementation of StreamResponse.stream_response function
import json
from typing import Any, AsyncIterator, Dict
from unittest.mock import AsyncMock, patch

import httpx
import pytest


class StreamResponse:
    async def stream_response(self, url: str, payload: Dict[str, Any], timeout: int = 30) -> AsyncIterator[Dict[str, Any]]:
        """Streams the response from the API, yielding each chunk as it's received."""
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", url, json=payload, timeout=timeout) as response:
                    if response.status_code != 200:
                        raise Exception(f"Error: {response.status_code}, {await response.text()}")
                    
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                chunk = json.loads(line)
                                yield chunk
                                if chunk.get("done"):
                                    break
                            except json.JSONDecodeError as jde:
                                print(f"{line=}")
                                print(f"Error decoding JSON: {jde=}", line)
                                continue
                        else:
                            print("No line received")
        except httpx.TimeoutException as e:
            raise Exception(f"Request timed out: {e}") from e

##################################################
# TESTS
##################################################

@patch("httpx.AsyncClient", new_callable=AsyncMock)
async def test_stream_response_normal(mock_client):
    # Arrange
    url = "http://test.com"
    payload = {"key": "value"}
    expected_chunk = {"data": "chunk1"}
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.aiter_lines.return_value = [json.dumps(expected_chunk)]
    mock_client.return_value.__aenter__.return_value = mock_response

    # Act
    stream = StreamResponse().stream_response(url, payload)
    result = await stream.__anext__()

    # Assert
    assert result == expected_chunk

@patch("httpx.AsyncClient", new_callable=AsyncMock)
async def test_stream_response_error(mock_client):
    # Arrange
    url = "http://test.com"
    payload = {"key": "value"}
    mock_response = AsyncMock()
    mock_response.status_code = 400
    mock_response.aiter_lines.return_value = []
    mock_client.return_value.__aenter__.return_value = mock_response

    # Act and Assert
    with pytest.raises(Exception):
        stream = StreamResponse().stream_response(url, payload)
        await stream.__anext__()

@patch("httpx.AsyncClient", new_callable=AsyncMock)
async def test_stream_response_timeout(mock_client):
    # Arrange
    url = "http://test.com"
    payload = {"key": "value"}
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.aiter_lines.side_effect = httpx.TimeoutException("Timeout occurred")
    mock_client.return_value.__aenter__.return_value = mock_response

    # Act and Assert
    with pytest.raises(Exception):
        stream = StreamResponse().stream_response(url, payload)
        await stream.__anext__()