import inspect
from typing import Any, List


class ClassDataModelFactory:
    @staticmethod
    def _get_init_parameters(class_to_process: Any) -> List[str]:
        """
        Returns a list of initialization parameters for the given class.

        Args:
            class_to_process (Any): The class to analyze.

        Returns:
            List[str]: A list of parameter names excluding 'self'.
        """
        init_signature = inspect.signature(class_to_process.__init__)
        return [param.name for param in init_signature.parameters.values() if param.name != "self"]

from unittest.mock import patch

import pytest

from code_autoeval.llm_model.utils.model.class_data_model import \
    ClassDataModelFactory


@pytest.mark.parametrize("class_to_process, expected", [
    (lambda x: None, []),  # No parameters
    (type('TestClass', (), {'__init__': lambda self, a, b: None}), ['a', 'b']),  # Two parameters
    (type('TestClassWithDefault', (), {'__init__': lambda self, a=1, b=2: None}), ['a', 'b']),  # With default values
])
def test_get_init_parameters(class_to_process, expected):
    """
    Test the _get_init_parameters method with different classes.
    """
    result = ClassDataModelFactory._get_init_parameters(class_to_process)
    assert sorted(result) == sorted(expected), f"Expected {expected}, but got {result}"

def test_no_self_parameter():
    """
    Test that 'self' is not included in the list of parameters.
    """
    class NoSelfParameter:
        def __init__(cls, a, b):
            pass

    result = ClassDataModelFactory._get_init_parameters(NoSelfParameter)
    assert "self" not in result, f"Expected 'self' to be excluded but was found in {result}"

def test_no_class_attributes():
    """
    Test that class attributes are not included.
    """
    class ClassWithAttribute:
        attr = 10
        def __init__(self, a, b):
            pass

    result = ClassDataModelFactory._get_init_parameters(ClassWithAttribute)
    assert "attr" not in result, f"Expected attribute 'attr' to be excluded but was found in {result}"

def test_no_base_classes():
    """
    Test that base class parameters are not included.
    """
    class BaseClass:
        def __init__(self, a):
            pass

    class DerivedClass(BaseClass):
        def __init__(self, b, **kwargs):
            super().__init__(**kwargs)

    result = ClassDataModelFactory._get_init_parameters(DerivedClass)
    assert "a" not in result, f"Expected base class parameter 'a' to be excluded but was found in {result}"

def test_mocked_class():
    """
    Test the function with a mocked class.
    """
    @patch("code_autoeval.llm_model.utils.model.class_data_model.ClassDataModelFactory.__init__", return_value=None)
    def mock_class(*args, **kwargs):
        pass

    result = ClassDataModelFactory._get_init_parameters(mock_class)
    assert result == [], f"Expected no parameters for the mocked class but got {result}"    assert result == [], f"Expected no parameters for the mocked class but got {result}"