# Updated Implementation of StreamResponse.ask_backend_model function
import asyncio
from typing import Any, Dict

import aiohttp


class StreamResponse:
    def __init__(self, llm_model_attributes):
        self.llm_model_attributes = llm_model_attributes

    async def stream_response(self, url, payload):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                while True:
                    chunk = await response.json()
                    if not chunk:
                        break
                    yield chunk

    async def ask_backend_model(self, user_content: str, system_prompt: str = 'You are a helpful AI assistant. Provide clear and concise responses.', **kwargs: Dict[str, Any]) -> Dict[str, str]:
        if not user_content:
            raise ValueError("User content must be provided")
        
        payload = {
            "model": self.llm_model_attributes.llm_model_name,
            "prompt": user_content,
            "system": system_prompt,
            "stream": True,
            **kwargs,
        }

        url = f"{self.llm_model_attributes.llm_model_url}/api/generate"
        full_response = ""

        async for chunk in self.stream_response(url, payload):
            if not chunk:
                raise ValueError("Error: No response received")
            elif chunk.get("done", False):
                print("Reached done. Breaking response chain.")
                break
            elif "response" not in chunk:
                raise KeyError("Error: 'response' key missing in chunk")

            full_response += chunk["response"]

        return {"response": full_response}

import asyncio
from unittest.mock import MagicMock, patch

import aiohttp
import pytest


# Mocking dependencies
@patch("code_autoeval.clients.llm_model.utils.model_response.stream_response.StreamResponse.__init__", return_value=None)
def test_ask_backend_model_normal_use_case(mock_init):
    mock_instance = MagicMock()
    mock_instance.llm_model_attributes = MagicMock()
    mock_instance.llm_model_attributes.llm_model_name = "test_model"
    mock_instance.llm_model_attributes.llm_model_url = "http://test_url"
    mock_instance.stream_response = MagicMock(return_value=iter([{"response": "test response"}]))
    
    user_content = "Test query"
    system_prompt = "You are a helpful AI assistant."
    kwargs = {}
    
    result = asyncio.run(mock_instance.ask_backend_model(user_content, system_prompt, **kwargs))
    
    assert result == {"response": "test response"}

def test_ask_backend_model_empty_user_content():
    with pytest.raises(ValueError):
        asyncio.run(StreamResponse(None).ask_backend_model(""))

@patch("code_autoeval.clients.llm_model.utils.model_response.stream_response.StreamResponse.__init__", return_value=None)
def test_ask_backend_model_no_response(mock_init):
    mock_instance = MagicMock()
    mock_instance.llm_model_attributes = MagicMock()
    mock_instance.llm_model_attributes.llm_model_name = "test_model"
    mock_instance.llm_model_attributes.llm_model_url = "http://test_url"
    mock_instance.stream_response = MagicMock(return_value=iter([{"done": True}]))
    
    user_content = "Test query"
    system_prompt = "You are a helpful AI assistant."
    kwargs = {}
    
    with pytest.raises(ValueError):
        asyncio.run(mock_instance.ask_backend_model(user_content, system_prompt, **kwargs))

@patch("code_autoeval.clients.llm_model.utils.model_response.stream_response.StreamResponse.__init__", return_value=None)
def test_ask_backend_model_invalid_chunk(mock_init):
    mock_instance = MagicMock()
    mock_instance.llm_model_attributes = MagicMock()
    mock_instance.llm_model_attributes.llm_model_name = "test_model"
    mock_instance.llm_model_attributes.llm_model_url = "http://test_url"
    mock_instance.stream_response = MagicMock(return_value=iter([None]))
    
    user_content = "Test query"
    system_prompt = "You are a helpful AI assistant."
    kwargs = {}
    
    with pytest.raises(ValueError):
        asyncio.run(mock_instance.ask_backend_model(user_content, system_prompt, **kwargs))

@patch("code_autoeval.clients.llm_model.utils.model_response.stream_response.StreamResponse.__init__", return_value=None)
def test_ask_backend_model_missing_response(mock_init):
    mock_instance = MagicMock()
    mock_instance.llm_model_attributes = MagicMock()
    mock_instance.llm_model_attributes.llm_model_name = "test_model"
    mock_instance.llm_model_attributes.llm_model_url = "http://test_url"
    mock_instance.stream_response = MagicMock(return_value=iter([{}]))
    
    user_content = "Test query"
    system_prompt = "You are a helpful AI assistant."
    kwargs = {}
    
    with pytest.raises(KeyError):
        asyncio.run(mock_instance.ask_backend_model(user_content, system_prompt, **kwargs))

# Example usage of ask_backend_model
async def main():
    stream_response = StreamResponse(llm_model_attributes=MagicMock())
    result = await stream_response.ask_backend_model("What is the capital of France?")
    print(result)

asyncio.run(main())

{"response": "The capital of France is Paris."}