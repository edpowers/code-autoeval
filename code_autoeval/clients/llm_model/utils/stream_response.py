"""Stream the response from the backend model."""


import json
import os
from typing import Any, AsyncIterator, Dict

import httpx
from dotenv import load_dotenv


class StreamResponse():
    """Stream response from the backend model."""

    def __init__(self) -> None:
        """Initialize the LLM Backend Client Model."""
        self._model = None
        self._model_url = self._instantiate_model_url()

    def _instantiate_model_url(self) -> str:
        """Instantiate the model URL."""
        load_dotenv()
        return os.getenv("OPENAI_BASE_URL", "")


    async def ask_backend_model(
        self,
        user_content: str,
        system_prompt: str = "You are a helpful AI assistant. Provide clear and concise responses.",
        model: str = "coder-lite:latest",
        **kwargs: Dict[str, Any],
    ) -> Dict[str, str]:
        """
        Queries the DeepSeek Coder model using the chat completion endpoint.

        Args:
        user_content (str): The user's input query.
        system_prompt (str): The system prompt to guide the model's behavior.
        model (str): The name of the model to use.
        **kwargs: Additional keyword arguments to pass to the API.

        Returns:
        Dict[str, str]: A dictionary containing the full response from the model.
        """
        payload = {
            "model": model,
            "prompt": user_content,
            "system": system_prompt,
            "stream": True,
            **kwargs,
        }

        url = f"{self._model_url}/api/generate"
        full_response = ""

        async for chunk in self.stream_response(url, payload):
            if not chunk:
                raise ValueError(f"Error: {chunk=}")
            elif chunk.get("done", ""):
                print("Reached done. Breaking response chain.")
                break
            elif not chunk.get("response", ""):
                raise KeyError(f"Error: {chunk=}")

            full_response += chunk["response"]

        return {"response": full_response}


    async def stream_response(
    self, url: str, payload: Dict[str, Any]
) -> AsyncIterator[Dict[str, Any]]:
        """Streams the response from the API, yielding each chunk as it's received.

        Args:
        url (str): The API endpoint URL.
        payload (Dict[str, Any]): The payload to send with the POST request.

        Yields:
        Dict[str, Any]: Each chunk of the response.

        Raises:
        Exception: If the HTTP status code is not 200.
        """
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url, json=payload) as response:
                if response.status_code != 200:
                    raise Exception(
                        f"Error: {response.status_code}, {await response.text()}"
                    )

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