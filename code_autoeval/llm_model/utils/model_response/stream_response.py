"""Stream the response from the backend model."""

import json
import re
from pprint import pprint
from typing import Any, AsyncIterator, Dict, Tuple

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
                    error_content = await response.aread()  # Read the entire response
                    raise Exception(
                        f"Error: {response.status_code}, {error_content.decode()}"
                    )

                buffer = b""
                async for chunk in response.aiter_bytes():
                    buffer += chunk
                    while b"\n" in buffer:
                        line, buffer = buffer.split(b"\n", 1)
                        if line:
                            try:
                                yield json.loads(line.decode())
                            except json.JSONDecodeError as jde:
                                print(f"Error decoding JSON: {jde}", line.decode())
                                continue

                if buffer:
                    try:
                        yield json.loads(buffer.decode())
                    except json.JSONDecodeError as jde:
                        print(f"Error decoding JSON: {jde}", buffer.decode())

    def figure_out_model_response(self, response: Any) -> str:
        """
        Extract the content from the model's response.
        """
        if isinstance(response, str):
            return response
        elif isinstance(response, dict):
            if "response" in response:
                return response["response"]
            elif "content" in response:
                return response["content"]
        raise ValueError(f"Unexpected response format from the model: {response}")

    def split_content_from_model(
        self,
        content: str,
    ) -> Tuple[str, str]:
        # Search for # Tests or 'pytest tests' in code:
        if not re.search("# Test|pytest tests|test", content):
            pprint(content)
            raise ValueError(
                "No '# Tests' provided in the model response. Unable to parse regex."
            )

        # Define the minimum character count (you can change this value as needed)
        min_char_count = 500
        # Modified regex pattern
        pattern = r"```(?:python)?(.{" + str(min_char_count) + r",}?)```"
        if code_blocks := re.findall(pattern, content, re.DOTALL):
            print(f"{code_blocks}", "Code blocks:")
            # If the code blocks are each longer than 500 characters:
            # Combine all code blocks, each separated by a newline
            code = "\n\n".join(block.strip() for block in code_blocks)
        else:
            code = content

        # Look for any class definitions. If not found, then just return the code and pytest_tests as the same.
        class_def_exists = re.search(r"class [A-Z]{5,}", code)
        if not class_def_exists:
            return code.strip(), code.strip()

        if "### Explanation:" in code:
            code_parts = re.split(r"### Explanation:", code, maxsplit=1)
            code = code_parts[0]

        return code.strip(), code.strip()
