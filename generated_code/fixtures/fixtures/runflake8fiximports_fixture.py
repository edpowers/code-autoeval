from unittest.mock import MagicMock

import pytest

from code_autoeval.llm_model.imports.run_flake8_fix_imports import RunFlake8FixImports


@pytest.fixture
def fixture_mock_runflake8fiximports():
    mock = MagicMock(spec=RunFlake8FixImports)
    mock.add_to_import_lines_from_original_imports = MagicMock()
    mock.combine_new_import_lines = MagicMock()
    mock.fix_remaining_import_statements = MagicMock()
    mock.parse_flake8_output = MagicMock()
    mock.add_class_import_to_file = MagicMock()
    mock.run_flake8_against_code = MagicMock()
    mock.run_flake8_pipeline_with_temp_file = classmethod(MagicMock())
    setattr(
        mock,
        "run_flake8_pipeline_with_temp_file",
        classmethod(getattr(mock, "run_flake8_pipeline_with_temp_file").__func__),
    )
    mock.run_flake_fix_imports = classmethod(MagicMock())
    setattr(
        mock,
        "run_flake_fix_imports",
        classmethod(getattr(mock, "run_flake_fix_imports").__func__),
    )
    return mock
