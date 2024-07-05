from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from code_autoeval.llm_model.utils.execute_generated_code import ExecuteGeneratedCode

# Analyze of the function:
# The function `find_args_for_generated_function` is designed to find and return arguments for a given generated function.
# It uses inspect.signature to get the signature of the function, then iterates over its parameters to determine which ones should be passed as arguments.
# If 'df' is one of the parameters, it checks if df is provided and appends the first column of df if so. For other cases, it either uses default values or raises errors based on the parameter type and presence of a default value.
# The function also includes debug prints when enabled.


def test_find_args_for_generated_function():
    # Mock data
    mock_df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})

    @patch(
        "code_autoeval.llm_model.utils.execute_generated_code.ExecuteGeneratedCode.__init__",
        return_value=None,
    )
    def test_normal_use(mock_init):
        mock_instance = ExecuteGeneratedCode({})

        # Test case 1: Normal use with 'df' as a parameter
        @patch("code_autoeval.llm_model.utils.execute_generated_code.inspect")
        def test(mock_inspect):
            mock_sig = MagicMock()
            mock_sig.parameters = {"df": MagicMock()}
            mock_inspect.signature.return_value = mock_sig

            result = mock_instance.find_args_for_generated_function(
                lambda x: None, mock_df
            )
            assert result == [mock_df]

        test()

    test_normal_use()


def test_edge_case_no_parameters():
    # Test case 2: Function with no parameters
    @patch(
        "code_autoeval.llm_model.utils.execute_generated_code.ExecuteGeneratedCode.__init__",
        return_value=None,
    )
    @patch("code_autoeval.llm_model.utils.execute_generated_code.inspect")
    def test(mock_inspect):
        mock_sig = MagicMock()
        mock_sig.parameters = {}
        mock_inspect.signature.return_value = mock_sig

        mock_instance = ExecuteGeneratedCode({})
        result = mock_instance.find_args_for_generated_function(
            lambda x: None, pd.DataFrame()
        )
        assert result == []

    test()


def test_error_case_df_not_provided():
    # Test case 3: Function with 'df' as a parameter but not provided
    @patch(
        "code_autoeval.llm_model.utils.execute_generated_code.ExecuteGeneratedCode.__init__",
        return_value=None,
    )
    @patch("code_autoeval.llm_model.utils.execute_generated_code.inspect")
    def test(mock_inspect):
        mock_sig = MagicMock()
        mock_sig.parameters = {"df": MagicMock()}
        mock_inspect.signature.return_value = mock_sig

        mock_instance = ExecuteGeneratedCode({})
        with pytest.raises(ValueError) as excinfo:
            mock_instance.find_args_for_generated_function(lambda x: None, None)
        assert str(excinfo.value) == "DataFrame is required but not provided"

    test()


def test_debug_print():
    # Test case 4: Debug print enabled
    @patch(
        "code_autoeval.llm_model.utils.execute_generated_code.ExecuteGeneratedCode.__init__",
        return_value=None,
    )
    @patch("code_autoeval.llm_model.utils.execute_generated_code.inspect")
    def test(mock_inspect):
        mock_sig = MagicMock()
        mock_sig.parameters = {"df": MagicMock()}
        mock_inspect.signature.return_value = mock_sig

        with patch("builtins.print") as mock_print:
            mock_instance = ExecuteGeneratedCode({})
            result = mock_instance.find_args_for_generated_function(
                lambda x: None, pd.DataFrame(), debug=True
            )
            assert result == []
            mock_print.assert_called_with(
                "Calling <lambda> with args: [DataFrame([], columns=['col1', 'col2'])"
            )

    test()


def test_skip_special_parameters():
    # Test case 5: Skipping '*args' and '**kwargs' parameters
    @patch(
        "code_autoeval.llm_model.utils.execute_generated_code.ExecuteGeneratedCode.__init__",
        return_value=None,
    )
    @patch("code_autoeval.llm_model.utils.execute_generated_code.inspect")
    def test(mock_inspect):
        mock_sig = MagicMock()
        mock_sig.parameters = {
            "arg1": MagicMock(),
            "arg2": MagicMock(),
            "*args": MagicMock(),
            "**kwargs": MagicMock(),
        }
        mock_inspect.signature.return_value = mock_sig

        mock_instance = ExecuteGeneratedCode({})
        result = mock_instance.find_args_for_generated_function(
            lambda *args, **kwargs: None
        )
        assert result == []

    test()
    test()
