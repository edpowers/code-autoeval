"""Class for deciphering/understanding model response."""

import json
import re


class DeciperResponse:
    """Class for deciphering/understanding model response."""


    def figure_out_model_response(self, c: dict) -> str:
        response = c["response"]

        if tool_output_match := re.search(
            r"<｜tool▁output▁begin｜>(.*?)<｜tool▁output▁end｜>",
            response,
            re.DOTALL,
        ):
            content = tool_output_match[1]
            try:
                content = json.loads(content)["response"]
            except json.JSONDecodeError:
                pass  # If JSON parsing fails, use the content as is
        elif json_match := re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL):
            try:
                content = json.loads(json_match[1])["response"]
            except json.JSONDecodeError:
                content = response  # If JSON parsing fails, use the full response
        else:
            content = response  # If no JSON found, use the full response

        # Clean up the content
        content = re.sub(r"<｜.*?｜>", "", content)  # Remove any remaining special tokens
        content = content.strip()  # Remove leading/trailing whitespace

        return content