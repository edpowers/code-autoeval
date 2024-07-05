from pathlib import Path
from unittest.mock import MagicMock, patch


from code_autoeval.llm_model.utils.base_llm_class import \
    CommonAttributesFactory


def test_create():
    # Arrange
    mock_project_root = Path("/path/to/project")
    mock_generated_base_dir = mock_project_root / "generated_code"

    with patch("code_autoeval.llm_model.utils.FindProjectRoot.find_project_root", return_value=mock_project_root):
        factory = CommonAttributesFactory()

        # Act
        result = factory.create()

        # Assert
        assert isinstance(result, MagicMock)
        assert result.project_root == mock_project_root
        assert result.generated_base_dir == mock_generated_base_dir

def test_create_with_mocked_dependencies():
    # Arrange
    mock_project_root = Path("/path/to/project")
    mock_generated_base_dir = mock_project_root / "generated_code"

    with patch("code_autoeval.llm_model.utils.FindProjectRoot.find_project_root", return_value=mock_project_root):
        factory = CommonAttributesFactory()

        # Act
        result = factory.create()

        # Assert
        assert isinstance(result, MagicMock)
        assert result.project_root == mock_project_root
        assert result.generated_base_dir == mock_generated_base_dir        assert isinstance(result, MagicMock)
        assert result.project_root == mock_project_root
        assert result.generated_base_dir == mock_generated_base_dir