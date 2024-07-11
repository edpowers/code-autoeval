"""Find/Classify function arguments."""

import inspect
from typing import Any, Callable, Dict, List, Optional

import pandas as pd


class FunctionArgumentFinder:
    """
    Example
    -------
    >>> def example_func(
        df: pd.DataFrame, column: str, multiplier: int = 2, *args, **kwargs
    ):
        pass

    >>> finder = FunctionArgumentFinder()
    >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    >>> args = finder.find_args(example_func, df, multiplier=3, extra_arg="test")
    >>> print(f"Final arguments: {args}")

    """

    def __init__(self, logger: Optional[Callable] = None):
        self.logger = logger or print

    def find_args(
        self, func: Callable, df: Optional[pd.DataFrame] = None, **kwargs
    ) -> List[Any]:
        """
        Find and prepare arguments for the given function.

        :param func: The function to prepare arguments for.
        :param df: Optional DataFrame to use for data-related parameters.
        :param kwargs: Additional keyword arguments to pass to the function.
        :return: List of arguments for the function.
        """
        sig = inspect.signature(func)
        args = []

        for param_name, param in sig.parameters.items():
            arg_value = self._resolve_argument(param_name, param, df, kwargs)
            if arg_value is not inspect.Parameter.empty:
                args.append(arg_value)

        self._log(f"Arguments for the function: {args}")
        return args

    def _resolve_argument(
        self,
        param_name: str,
        param: inspect.Parameter,
        df: Optional[pd.DataFrame],
        kwargs: Dict[str, Any],
    ) -> Any:
        """Resolve the value for a single argument."""
        if param_name in kwargs:
            return kwargs[param_name]
        elif param_name == "df" and df is not None:
            return df
        elif param.annotation == pd.DataFrame and df is not None:
            return df
        elif param.annotation == str and df is not None and len(df.columns) > 0:
            return df.columns[0]
        elif param.default != inspect.Parameter.empty:
            return param.default
        elif param.kind == inspect.Parameter.VAR_POSITIONAL:
            return tuple()
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            return {}
        elif param.annotation in (int, float, bool, str):
            return self._get_default_for_type(param.annotation)
        else:
            self._log(f"Unable to determine value for parameter '{param_name}'")
            return inspect.Parameter.empty

    def _get_default_for_type(self, annotation: type) -> Any:
        """Get a default value for basic types."""
        defaults = {int: 0, float: 0.0, bool: False, str: ""}
        return defaults.get(annotation)

    def _log(self, message: str):
        """Log a message using the provided logger or print function."""
        self.logger(message)
