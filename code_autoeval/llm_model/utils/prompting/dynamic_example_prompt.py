""""Dynamic example prompting."""

from typing import List, Optional

from multiuse.model import class_data_model

from code_autoeval.llm_model.utils.model import function_attributes


class DynamicExamplePrompt:
    """Dynamic example prompting.

    The name func_name refers to the full class name and method name.
    For example, if the class name is 'MyClass' and the method name is 'my_method',
    Then the following would be true:

    class_name = 'MyClass'
    method_name = 'my_method'
    func_name = 'MyClass.my_method'
    """

    def provide_test_structure(
        self,
        is_coroutine: bool,
        class_name: str,
        class_relative_path: str,
        func_name: str,
        method_name: str,
        function_params: List[str],
        init_params: List[str],
        function_return_type: str = "Any",
        class_model: Optional[class_data_model.ClassDataModel] = None,
        func_attributes: Optional[function_attributes.FunctionAttributes] = None,
    ) -> str:
        fixture_name = f"mock_{class_name.lower()}"
        test_name = f"test_{func_name}"
        fixture_setup = self.generate_fixture_setup(
            class_name,
            fixture_name,
            class_model.import_statement,
            func_name,
            method_name,
            function_return_type,
        )
        arrange = self.generate_arrange(
            class_name, method_name, init_params, function_params, fixture_name
        )
        act = self.generate_act(is_coroutine, func_name, method_name, function_params)
        assert_statements = self.generate_assert(
            func_name, method_name, function_return_type, function_params
        )

        test_function = f"""
{fixture_setup}

{'@pytest.mark.asyncio' if is_coroutine else ''}
{'async ' if is_coroutine else ''}def {test_name}({fixture_name}):
    # Arrange
{arrange}

    # Act
{act}

    # Assert
{assert_statements}
        """
        return test_function

    def generate_fixture_setup(
        self,
        class_name: str,
        fixture_name: str,
        import_statement: str,
        func_name: str,
        method_name: str,
        function_return_type: str,
        dependencies: List[str] = [],
    ) -> str:
        dependency_mocks = "\n    ".join(f"{dep} = MagicMock()" for dep in dependencies)
        return f"""
    import pytest
    from unittest.mock import MagicMock
    {import_statement}

    @pytest.fixture(scope='module')
    def {fixture_name}():
        {dependency_mocks}
        return {class_name}({', '.join(dependencies)})
        """

    def generate_arrange(
        self,
        class_name: str,
        method_name: str,
        init_params: List[str],
        function_params: List[str],
        fixture_name: str,
    ) -> str:
        param_setup = "".join(
            f"    {param} = {self.generate_sample_data(param)}\n"
            for param in function_params
        )
        return f"{param_setup}\n    instance = {fixture_name}"

    def generate_act(
        self,
        is_coroutine: bool,
        func_name: str,
        method_name: str,
        function_params: List[str],
    ) -> str:
        # Remove 'self' from function params if present and if method is not class method
        params = [
            param for param in function_params if str(param) not in {"self", "cls"}
        ]
        params_str = ", ".join(params)
        return f"    {'await ' if is_coroutine else ''}result = instance.{method_name}({params_str})"

    def generate_assert(
        self,
        method_name: str,
        function_return_type: str,
        function_params: List[str],
        expected_output: Optional[str] = None,
    ) -> str:
        """
        Generates assert statements for the test function.

        :param method_name: The name of the method being tested.
        :param function_return_type: The expected return type of the method.
        :param function_params: The parameters passed to the method.
        :param expected_output: The expected output of the method if applicable.
        :return: A string containing the assert statements.
        """
        assert_statements = f"    # Assert that the result is of the expected type\n"
        assert_statements += f"    assert isinstance(result, {function_return_type})\n"

        # Check if there's an expected output to assert
        if expected_output:
            assert_statements += (
                f"    # Assert that the result matches the expected output\n"
            )
            assert_statements += f"    assert result == {expected_output}\n"

        # Custom assertions based on the return type
        if function_return_type == "dict":
            assert_statements += """
        # Assert that the result is a dictionary and has expected keys
        assert 'type' in result
        assert result['type'] == 'DataFrame'
    """
        elif function_return_type == "pd.DataFrame":
            assert_statements += """
        # Assert that the result is a non-empty DataFrame
        assert not result.empty
        assert isinstance(result, pd.DataFrame)
    """
        elif function_return_type == "str":
            assert_statements += """
        # Assert that the result is a non-empty string
        assert isinstance(result, str)
        assert len(result) > 0
    """
        elif function_return_type == "int":
            assert_statements += """
        # Assert that the result is an integer and is non-negative (modify as needed)
        assert isinstance(result, int)
        assert result >= 0  # or any other condition that is expected
    """
        elif function_return_type == "float":
            assert_statements += """
        # Assert that the result is a float and is non-negative (modify as needed)
        assert isinstance(result, float)
        assert result >= 0.0  # or any other condition that is expected
    """
        elif function_return_type == "list":
            assert_statements += """
        # Assert that the result is a non-empty list
        assert isinstance(result, list)
        assert len(result) > 0  # or any other condition that is expected
    """
        elif function_return_type == "bool":
            assert_statements += """
        # Assert that the result is a boolean
        assert isinstance(result, bool)
    """
        elif function_return_type == "NoneType":
            assert_statements += """
        # Assert that the result is None
        assert result is None
    """
        return assert_statements

    def generate_init_test(self, class_name: str, init_params: List[str]) -> str:
        params = ", ".join(f"{param}=MagicMock()" for param in init_params)
        param_assertions = "\n    ".join(
            f"assert hasattr(instance, '{param}')" for param in init_params
        )
        return f"""
    def test_{class_name}_init(mock_{class_name.lower()}):
        # Arrange
        {params}

        # Act
        instance = mock_{class_name.lower()}({', '.join(init_params)})

        # Assert
        assert isinstance(instance, MagicMock)
        {param_assertions}
        mock_{class_name.lower()}.assert_called_once_with({', '.join(init_params)})
        """

    def generate_sample_data(self, param_name: str) -> str:
        if "df" in param_name.lower():
            return "pd.DataFrame({'A': range(10), 'B': range(10, 20)})"
        elif "dict" in param_name.lower():
            return "{'A': [1, 2], 'B': [3, 4]}"
        else:
            return "MagicMock()"

    # Currently unused.
    def generate_error_test(
        self,
        class_name: str,
        func_name: str,
        method_name: str,
        error_condition: str,
        expected_error: str,
    ) -> str:
        return f"""
def test_{method_name}_error_condition(mock_{class_name.lower()}):
    # Arrange
    instance = mock_{class_name.lower()}
    {error_condition}

    # Act & Assert
    with pytest.raises({expected_error}):
        instance.{method_name}({error_condition.split('=')[0].strip()})
"""

    def generate_mock_return_value(self, return_type: str) -> str:
        type_mapping = {
            "str": '"example_string"',
            "int": "42",
            "float": "3.14",
            "bool": "True",
            "list": "[1, 2, 3]",
            "dict": '{"key": "value"}',
            "tuple": '(1, "two", 3.0)',
            "set": "{1, 2, 3}",
            "None": "None",
        }
        return type_mapping.get(return_type, f"MagicMock(spec={return_type})")
