import json
import re

        class DeciperResponse:
            def figure_out_model_response(self, c: dict) -> str:
                response = c["response"]

                if tool_output_match := re.search(r"(\[.*?\])", response, re.DOTALL):
                    content = tool_output_match[1]
                    try:
                        content = json.loads(content)["response"]
                    except json.JSONDecodeError:
                        pass  # If JSON parsing fails, use the content as is
                elif json_match := re.search(r"

", response, re.DOTALL):
                    try:
                        content = json.loads(json_match[1])["response"]
                    except json.JSONDecodeError:
                        content = response  # If JSON parsing fails, use the full response
                else:
                    content = response  # If no JSON found, use the full response

                # Clean up the content
                content = re.sub(r"", "", content)  # Remove any remaining special tokens
                content = content.strip()  # Remove leading/trailing whitespace

                return content

import json
from unittest.mock import patch

import pytest

        @pytest.fixture
        def decipher_response():
            return DeciperResponse()

        def test_normal_json_response(decipher_response):
            c = {"response": '{"response": "test response"}'}
            assert decipher_response.figure_out_model_response(c) == '"test response"'

        def test_json_in_codeblock_response(decipher_response):
            c = {"response": "

"}
            assert decipher_response.figure_out_model_response(c) == '"test response"'

        def test_no_json_found(decipher_response):
            c = {"response": "This is a plain text response."}
            assert decipher_response.figure_out_model_response(c) == "This is a plain text response."

        def test_invalid_json_in_codeblock(decipher_response):
            c = {"response": '