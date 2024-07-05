from unittest.mock import patch

import pytest


class FunctionAttributes:
    def __init__(self, func_name, is_coroutine, function_signature, function_docstring, function_body):
        self.func_name = func_name
        self.is_coroutine = is_coroutine
        self.function_signature = function_signature
        self.function_docstring = function_docstring
        self.function_body = function_body

class ClassDataModel:
    def __init__(self, absolute_path, base_classes, init_params, class_attributes):
        self.absolute_path = absolute_path
        self.base_classes = base_classes
        self.init_params = init_params
        self.class_attributes = class_attributes

class SystemPrompts:
    def return_analyis_and_guidelines(self):
        return "This function generates a system prompt based on the provided query and goal."

    async def generate_system_prompt_with_existing_function(self, query: str, goal: str, function_attributes: FunctionAttributes, class_model: ClassDataModel) -> str:
        # Mocking __init__ functions should return None
        @patch("code_autoeval.llm_model.llm_model.LLMModel.__init__", return_value=None)
        def mock_init(self, *args, **kwargs):
            pass

        # Example usage of the function
        if function_attributes.is_coroutine:
            @pytest.mark.asyncio
            async def test_generate_system_prompt_with_existing_function():
                result = await self.generate_system_prompt_with_existing_function("query", "goal", FunctionAttributes("func_name", True, "signature", "docstring", "body"), ClassDataModel("path", ["base"], ["args", "kwargs"], []))
                assert result == """You are an expert Python code analyst and test writer.
Your task is to analyze an existing Python function and create comprehensive tests for it."""
        else:
            def test_generate_system_prompt_with_existing_function():
                result = self.generate_system_prompt_with_existing_function("query", "goal", FunctionAttributes("func_name", False, "signature", "docstring", "body"), ClassDataModel("path", ["base"], ["args", "kwargs"], []))
                assert result == """You are an expert Python code analyst and test writer.
Your task is to analyze an existing Python function and create comprehensive tests for it."""

        return f"""
        You are an expert Python code analyst and test writer.
        Your task is to analyze an existing Python function and create comprehensive tests for it.

        1. Function Details:
        Function Name: {function_attributes.func_name}
        Function is async coroutine: {function_attributes.is_coroutine}
        Signature: {function_attributes.function_signature}
        Docstring: {function_attributes.function_docstring}
        Function Body:
        {function_attributes.function_body}

        If there are base classes, initialization parameters, or class attributes,
        please mock all of the dependencies so that we can properly unit test.
        Use unittest.mock or any other pytest.patch method to mock these dependencies.

        Please use the following relative path provided for all mocking:
        {class_model.absolute_path}

        Function Base Classes:
        {class_model.base_classes}

        Initialization Parameters:
        {class_model.init_params}

        Class Attributes:
        {class_model.class_attributes}

        Mocking __init__ functions should return None, like the following:
        @patch("code_autoeval.llm_model.llm_model.LLMModel.__init__", return_value=None)

        2. Task: {query} - with {goal}

        {self.return_analyis_and_guidelines()}

        if {function_attributes.is_coroutine=}, then use pytest-asyncio to test async functions.
        For example:
        @pytest.mark.asyncio
        async def test_async_function():
            result = await your_async_function()
            assert result == expected_value

        5. Output Format:
        - Provide a brief analysis of the function (2-3 sentences).
        - Then, provide the pytest tests.

        Example of expected response format:

"""
"""