# Updated Implementation of ClassDataModelFactory._get_class_attributes function
from typing import Any, List


class ClassDataModelFactory:
    @staticmethod
    def _get_class_attributes(class_to_process: Any) -> List[str]:
        """
        Retrieve a list of class attributes that are not special methods (starting with '__') and are not callable.
        
        Args:
            class_to_process (Any): The class object from which to retrieve the attributes.
        
        Returns:
            List[str]: A list of attribute names.
        """
        if not isinstance(class_to_process, type) or not hasattr(class_to_process, '__dict__'):
            raise TypeError("Input must be a class object")
        
        return [name for name in dir(class_to_process) if not name.startswith("__") and not callable(getattr(class_to_process, name))]

from typing import Any, List
from unittest.mock import patch

import pytest


# Updated implementation of ClassDataModelFactory._get_class_attributes function
class ClassDataModelFactory:
    @staticmethod
    def _get_class_attributes(class_to_process: Any) -> List[str]:
        if not isinstance(class_to_process, type) or not hasattr(class_to_process, '__dict__'):
            raise TypeError("Input must be a class object")
        
        return [name for name in dir(class_to_process) if not name.startswith("__") and not callable(getattr(class_to_process, name))]

# Test cases for _get_class_attributes method
def test_normal_case():
    class ExampleClass:
        attr1 = 1
        __attr2 = "hidden"
        
        def method(self):
            pass
    
    expected_output = ['attr1']
    assert ClassDataModelFactory._get_class_attributes(ExampleClass) == expected_output

def test_no_attributes():
    class NoAttributes:
        pass
    
    expected_output = []
    assert ClassDataModelFactory._get_class_attributes(NoAttributes) == expected_output

def test_all_hidden_attributes():
    class HiddenAttributes:
        __attr1 = "hidden"
        __attr2__ = "also hidden"
        
        def method(self):
            pass
    
    expected_output = []
    assert ClassDataModelFactory._get_class_attributes(HiddenAttributes) == expected_output

def test_callable_methods():
    class CallableMethods:
        attr1 = 1
        
        def method(self):
            pass
    
    expected_output = ['attr1']
    assert ClassDataModelFactory._get_class_attributes(CallableMethods) == expected_output

def test_empty_input():
    class Empty:
        pass
    
    with pytest.raises(TypeError):
        ClassDataModelFactory._get_class_attributes(None)