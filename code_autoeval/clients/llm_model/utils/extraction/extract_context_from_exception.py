"""Extract the context from the exception."""

import traceback
from typing import Optional


class ExtractContextFromException:

    def format_error(
        self,
        exception: Exception,
        generated_code: Optional[str] = None,
        context_lines: int = 3,
    ) -> str:
        tb = traceback.extract_tb(exception.__traceback__)
        error_type = type(exception).__name__
        error_message = str(exception)

        # Get the most recent frame from the traceback
        last_frame = tb[-1]
        filename, line_number, func_name, text = last_frame

        formatted_description = f"""
        Error Type: {error_type}
        Error Message: {error_message}

        Error occurred in file: {filename}
        At line number: {line_number}
        In function: {func_name}

        Full traceback:
        {traceback.format_exc()}
        """
        if generated_code:
            relevant_code = self._get_relevant_code(
                generated_code, line_number, context_lines=context_lines
            )
            formatted_description += f"""
        Relevant code context:
        {relevant_code}

        Generated code that caused the error:
        {generated_code}
        """

        return formatted_description.strip()

    def _get_relevant_code(
        self, code: str, error_line: int, context_lines: int = 3
    ) -> str:
        code_lines = code.split("\n")
        start_line = max(0, error_line - context_lines - 1)
        end_line = min(len(code_lines), error_line + context_lines)

        relevant_lines = code_lines[start_line:end_line]

        # Add line numbers to the relevant code
        numbered_lines = [
            f"{i+start_line+1}: {line}" for i, line in enumerate(relevant_lines)
        ]
        return "\n".join(numbered_lines)

    def create_llm_error_prompt(self, formatted_error: str) -> str:
        return f"""
        The previous code generation attempt resulted in an error. Here are the details:

        {formatted_error}

        Please analyze this error and provide a corrected version of the code that addresses the issue.
        """
