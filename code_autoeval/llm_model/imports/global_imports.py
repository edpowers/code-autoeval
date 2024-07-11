"""Class for defining global imports (default)."""

import importlib
import inspect
import logging
import os
import re
import subprocess
import sys
import tempfile
from typing import Any, Dict, Set

import numpy as np
import pandas as pd

DEFAULT_GLOBAL_IMPORTS: Dict[str, Any] = {
    "pd": pd,
    "np": np,
    "logging": logging,  # Add logging explicitly
    "os": os,  # Add os explicitly
    "re": re,  # Add re explicitly
    "subprocess": subprocess,  # Add subprocess explicitly
    "sys": sys,  # Add sys explicitly
    "tempfile": tempfile,  # Add tempfile explicitly
    "importlib": importlib,  # Add importlib explicitly
    "inspect": inspect,  # Add inspect explicitly
}


class GlobalImports:
    """Define a base set of global imports."""

    @classmethod
    def create_global_imports(cls) -> "GlobalImports":
        """Create the global imports."""
        return cls()

    def __init__(self):
        self.imported_libraries: Set[str] = self.find_imports_from_env()
        self.default_global_imports: Dict[str, Any] = DEFAULT_GLOBAL_IMPORTS

    def run_global_imports(self) -> Dict[str, Any]:
        """Run the global imports."""
        self._import_libraries(set(self.default_global_imports.values()))

        return self.return_global_vars()

    def return_global_vars(self) -> Dict[str, Any]:
        """Return the global variables."""
        return self.default_global_imports

    def find_imports_from_env(self) -> Set[str]:
        return {self._extract_sys_module_prefix(mod) for mod in sys.modules}

    def _extract_sys_module_prefix(self, lib: str) -> str:
        return lib.split(".")[0]

    def _import_libraries(self, libraries: set) -> None:
        """Import the required libraries."""
        for lib in libraries:
            if lib not in self.imported_libraries:
                importlib.import_module(lib)

        self.find_imports_from_env()
