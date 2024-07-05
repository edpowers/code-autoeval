import pytest
from unittest.mock import patch
from code_autoeval.clients.llm_model.utils.execute_generated_code import ExecuteGeneratedCode

# Test data
normal_func = lambda x: x
local_vars = {'normal_func': normal_func}

edge_case_func = None
invalid_local_vars = {}

error_func_name = 'non_existent_func'

@pytest.mark.parametrize("func, local_vars, expected", [
    (normal_func, local_vars, 'normal_func'),
])
def test_find_func_name_normal(func, local_vars, expected):
    instance = ExecuteGeneratedCode()
    result = instance._find_func_name(func, local_vars)
    assert result == expected

@pytest.mark.parametrize("func, local_vars", [
    (edge_case_func, local_vars),
    (normal_func, invalid_local_vars),
])
def test_find_func_name_edge_and_error(func, local_vars):
    instance = ExecuteGeneratedCode()
    with pytest.raises(ValueError):
        instance._find_func_name(func, local_vars)

@pytest.mark.parametrize("func, local_vars", [
    (normal_func, {'non_callable': 'not callable'}),
])
def test_find_func_name_invalid_callable(func, local_vars):
    instance = ExecuteGeneratedCode()
    with pytest.raises(ValueError):
        instance._find_func_name(func, local_vars)