from unittest.mock import patch

import pytest
from code_autoeval.clients.llm_model.utils.validation.validate_regexes import ValidateRegexes

# Function Analysis:
# The function `validate_class_name_in_local_vars` checks if a given class name is present in the local variables dictionary.
# If not, it raises a ValueError with an appropriate message.

def test_normal_case():
    # Arrange
    class_name = "ParentClass"
    local_vars = {"ParentClass": object}
    
    # Act and Assert
    assert ValidateRegexes.validate_class_name_in_local_vars(None, class_name, local_vars) is None

def test_missing_class():
    # Arrange
    class_name = "NonExistentClass"
    local_vars = {"ExistingClass": object}
    
    # Act and Assert
    with pytest.raises(ValueError):
        ValidateRegexes.validate_class_name_in_local_vars(None, class_name, local_vars)

def test_none_class_name():
    # Arrange
    class_name = None
    local_vars = {"ExistingClass": object}
    
    # Act and Assert
    with pytest.raises(TypeError):
        ValidateRegexes.validate_class_name_in_local_vars(None, class_name, local_vars)

def test_none_local_vars():
    # Arrange
    class_name = "ParentClass"
    local_vars = None
    
    # Act and Assert
    with pytest.raises(TypeError):
        ValidateRegexes.validate_class_name_in_local_vars(None, class_name, local_vars)

def test_empty_local_vars():
    # Arrange
    class_name = "ParentClass"
    local_vars = {}
    
    # Act and Assert
    with pytest.raises(ValueError):
        ValidateRegexes.validate_class_name_in_local_vars(None, class_name, local_vars)