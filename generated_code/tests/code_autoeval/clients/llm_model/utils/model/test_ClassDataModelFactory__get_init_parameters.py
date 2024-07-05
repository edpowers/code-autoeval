from unittest.mock import patch

import pytest
from code_autoeval.clients.llm_model.utils.model.class_data_model import ClassDataModelFactory


@pytest.fixture(name="mocked_class")
def fixture_mocked_class():
    class MockClass:
        def __init__(self, project_root, another_param):
            pass
    return MockClass

def test_get_init_parameters_normal(mocked_class):
    with patch("code_autoeval.clients.llm_model.utils.model.class_data_model.inspect") as mock_inspect:
        mock_signature = mock_inspect.signature.return_value
        mock_signature.parameters = {'self': None, 'project_root': None, 'another_param': None}
        
        result = ClassDataModelFactory._get_init_parameters(mocked_class)
        
        assert result == ['project_root', 'another_param']

def test_get_init_parameters_no_params():
    class NoParamsClass:
        def __init__(self):
            pass
    
    with patch("code_autoeval.clients.llm_model.utils.model.class_data_model.inspect") as mock_inspect:
        mock_signature = mock_inspect.signature.return_value
        mock_signature.parameters = {'self': None}
        
        result = ClassDataModelFactory._get_init_parameters(NoParamsClass)
        
        assert result == []

def test_get_init_parameters_only_self():
    class OnlySelfClass:
        def __init__(self):
            pass
    
    with patch("code_autoeval.clients.llm_model.utils.model.class_data_model.inspect") as mock_inspect:
        mock_signature = mock_inspect.signature.return_value
        mock_signature.parameters = {'self': None}
        
        result = ClassDataModelFactory._get_init_parameters(OnlySelfClass)
        
        assert result == []

def test_get_init_parameters_with_other_methods():
    class OtherMethodsClass:
        def __init__(self, project_root, another_param):
            pass
        def some_method(self):
            pass
    
    with patch("code_autoeval.clients.llm_model.utils.model.class_data_model.inspect") as mock_inspect:
        mock_signature = mock_inspect.signature.return_value
        mock_signature.parameters = {'self': None, 'project_root': None, 'another_param': None}
        
        result = ClassDataModelFactory._get_init_parameters(OtherMethodsClass)
        
        assert result == ['project_root', 'another_param']

def test_get_init_parameters_with_base_classes():
    class BaseClass:
        def __init__(self, base_param):
            pass
    
    class DerivedClass(BaseClass):
        def __init__(self, project_root, another_param, base_param):
            super().__init__(base_param)
            self.project_root = project_root
            self.another_param = another_param
    
    with patch("code_autoeval.clients.llm_model.utils.model.class_data_model.inspect") as mock_inspect:
        mock_signature = mock_inspect.signature.return_value
        mock_signature.parameters = {'self': None, 'project_root': None, 'another_param': None, 'base_param': None}
        
        result = ClassDataModelFactory._get_init_parameters(DerivedClass)
        
        assert result == ['project_root', 'another_param']