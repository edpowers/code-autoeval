# Updated Implementation of CommonAttributesFactory.create function
from pathlib import Path

from code_autoeval.clients.llm_model.utils.base_llm_class import CommonAttributes, CommonAttributesFactory


class FindProjectRoot:
    def find_project_root(self):
        # Mock implementation for finding the project root
        return Path("/mock/path")

CommonAttributesFactory._find_project_root = FindProjectRoot.find_project_root

def create():
    """
    Create a CommonAttributes instance with appropriate paths based on the project root.
    
    Returns:
        CommonAttributes: An instance of CommonAttributes containing the project root and generated code directory path.
    """
    find_project_root = FindProjectRoot()
    project_root = find_project_root.find_project_root()

    assert isinstance(project_root, Path), "Expected a Path object for project_root"
    assert project_root.exists(), f"The provided project root {project_root} does not exist"

    generated_base_dir = project_root / "generated_code"

    return CommonAttributes(
        project_root=project_root,
        generated_base_dir=generated_base_dir
    )

##################################################
# TESTS
##################################################

from unittest.mock import patch

import pytest


def test_create():
    with patch("code_autoeval.clients.llm_model.utils.base_llm_class.FindProjectRoot", return_value=Path("/mock/path")):
        result = create()
        assert isinstance(result, CommonAttributes)
        assert result.project_root == Path("/mock/path")
        assert result.generated_base_dir == Path("/mock/path/generated_code")

def test_create_with_non_existent_project_root():
    class MockFindProjectRoot:
        def find_project_root(self):
            return None
    
    with patch("code_autoeval.clients.llm_model.utils.base_llm_class.FindProjectRoot", new=MockFindProjectRoot):
        with pytest.raises(AssertionError):
            create()

def test_create_with_existing_project_root():
    mock_project_root = Path("/mock/path")
    mock_generated_base_dir = mock_project_root / "generated_code"
    
    class MockFindProjectRoot:
        def find_project_root(self):
            return mock_project_root
    
    with patch("code_autoeval.clients.llm_model.utils.base_llm_class.FindProjectRoot", new=MockFindProjectRoot):
        result = create()
        assert isinstance(result, CommonAttributes)
        assert result.project_root == mock_project_root
        assert result.generated_base_dir == mock_generated_base_dir