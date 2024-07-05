import subprocess
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
from code_autoeval.clients.llm_model.utils.code_cleaning.run_pyflakes_isort import RunPyflakesIsort


def test_normal_use_case():
    code = "import os\nprint('Hello, World!')"
    max_line_length = 88
    run_pyflakes_isort = RunPyflakesIsort()
    
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = code
        result = run_pyflakes_isort.run_pyflakes_isort_pipeline(code, max_line_length)
        
        assert result[0] == code
        assert result[1] is True

def test_no_modification():
    code = "import os\nprint('Hello, World!')"
    max_line_length = 88
    run_pyflakes_isort = RunPyflakesIsort()
    
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = code
        result = run_pyflakes_isort.run_pyflakes_isort_pipeline(code, max_line_length)
        
        assert result[0] == code
        assert result[1] is False

def test_error_in_isort():
    code = "import os\nprint('Hello, World!')"
    max_line_length = 88
    run_pyflakes_isort = RunPyflakesIsort()
    
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        result = run_pyflakes_isort.run_pyflakes_isort_pipeline(code, max_line_length)
        
        assert result[0] == code
        assert result[1] is False

def test_error_in_pyflakes():
    code = "import os\nprint('Hello, World!')"
    max_line_length = 88
    run_pyflakes_isort = RunPyflakesIsort()
    
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = ""
        mock_run.return_value.returncode = 1
        result = run_pyflakes_isort.run_pyflakes_isort_pipeline(code, max_line_length)
        
        assert result[0] == code
        assert result[1] is False

def test_empty_code():
    code = ""
    max_line_length = 88
    run_pyflakes_isort = RunPyflakesIsort()
    
    with patch("subprocess.run") as mock_run:
        result = run_pyflakes_isort.run_pyflakes_isort_pipeline(code, max_line_length)
        
        assert result[0] == code
        assert result[1] is True