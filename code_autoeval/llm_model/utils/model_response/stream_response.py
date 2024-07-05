"""Stream the response from the backend model."""

import json
from typing import Any, AsyncIterator, Dict

import httpx

from code_autoeval.llm_model.utils.base_llm_class import BaseLLMClass


class StreamResponse(BaseLLMClass):
    """Stream response from the backend model."""

    # No need for __init__ method anymore, as ModelAttributes are initialized by default

    async def ask_backend_model(
        self,
        user_content: str,
        system_prompt: str = "You are a helpful AI assistant. Provide clear and concise responses.",
        **kwargs: Dict[str, Any],
    ) -> Dict[str, str]:
        """
        Queries the DeepSeek Coder model using the chat completion endpoint.

        Args:
        user_content (str): The user's input query.
        system_prompt (str): The system prompt to guide the model's behavior.
        **kwargs: Additional keyword arguments to pass to the API.

        Returns:
        Dict[str, str]: A dictionary containing the full response from the model.
        """
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
                raise ValueError(f"Error: {chunk=}")
            elif chunk.get("done", ""):
                print("Reached done. Breaking response chain.")
                break
            elif not chunk.get("response", ""):
                raise KeyError(f"Error: {chunk=}")

            full_response += chunk["response"]

        return {"response": full_response}

    async def stream_response(
        self,
        url: str,
        payload: Dict[str, Any],
        timeout: int = 30,
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
            async with client.stream(
                "POST", url, json=payload, timeout=timeout
            ) as response:
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
