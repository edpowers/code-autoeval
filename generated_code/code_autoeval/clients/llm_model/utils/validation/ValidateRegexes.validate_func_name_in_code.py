import pytest
from unittest.mock import patch
from pprint import pprint

class ValidateRegexes:
    def validate_func_name_in_code(self, code: str, func_name: str) -> None:
        if ".__init__" in func_name:
            func_name = func_name.split(".__init__")[0]
        
        # Accomodate for the fact that the function name may be in the form of "class_name.func_name"
        if "." in func_name:
            func_name = func_name.split(".")[-1]
        
        if func_name not in code:
            pprint(code)
            raise ValueError(f"Function name '{func_name}' not found in the formatted code.")

import pytest
from unittest.mock import patch
from pprint import pprint

class ValidateRegexes:
    def validate_func_name_in_code(self, code: str, func_name: str) -> None:
        if ".__init__" in func_name:
            func_name = func_name.split(".__init__")[0]
        
        # Accomodate for the fact that the function name may be in the form of "class_name.func_name"
        if "." in func_name:
            func_name = func_name.split(".")[-1]
        
        if func_name not in code:
            pprint(code)
            raise ValueError(f"Function name '{func_name}' not found in the formatted code.")

##################################################
# TESTS
##################################################

@pytest.fixture
def validate_regexes():
    return ValidateRegexes()

def test_validate_func_name_in_code_normal(validate_regexes):
    # Normal case: function name is in the code
    code = "def my_function():\n    pass"
    func_name = "my_function"
    validate_regexes.validate_func_name_in_code(code, func_name)
    assert True  # No exception raised

def test_validate_func_name_in_code_missing(validate_regexes):
    # Case where function name is not in the code
    code = "def another_function():\n    pass"
    func_name = "my_function"
    with pytest.raises(ValueError):
        validate_regexes.validate_func_name_in_code(code, func_name)

def test_validate_func_name_in_code_init(validate_regexes):
    # Case where function name is part of __init__ method
    code = "class MyClass:\n    def __init__(self):\n        pass\n"
    func_name = "MyClass.__init__"
    validate_regexes.validate_func_name_in_code(code, func_name)
    assert True  # No exception raised

def test_validate_func_name_in_code_class_method(validate_regexes):
    # Case where function name is a method of a class
    code = "class MyClass:\n    def my_function():\n        pass"
    func_name = "MyClass.my_function"
    validate_regexes.validate_func_name_in_code(code, func_name)
    assert True  # No exception raised

def test_validate_func_name_in_code_empty_code(validate_regexes):
    # Case where code is empty
    code = ""
    func_name = "my_function"
    with pytest.raises(ValueError):
        validate_regexes.validate_func_name_in_code(code, func_name)

plaintext
Traceback (most recent call last):
  File "your_script.py", line XX, in test_validate_func_name_in_code_missing
    validate_regexes.validate_func_name_in_code(code, func_name)
  File "your_script.py", line YY, in validate_func_name_in_code
    raise ValueError(f"Function name '{func_name}' not found in the formatted code.")
ValueError: Function name 'my_function' not found in the formatted code.