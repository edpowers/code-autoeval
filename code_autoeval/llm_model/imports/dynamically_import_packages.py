"""Dynamically import packages from file."""

# Assumes that the file is a Python file and is generated during
# runtime - therefore if there are any modules that aren't already
# imported, we will need to import them dynamically.

import importlib
import os
import subprocess
import sys
import tempfile
from typing import Optional, Set

from pydantic import Field

from code_autoeval.llm_model.utils.log_funcs import logging_funcs

# TODO - Figure out proper methods of testing this.


class DynamicallyImportPackages(logging_funcs.LoggingFuncs):

    imported_libraries: Set[str] = Field(default_factory=set)

    @classmethod
    def import_required_libraries(
        cls, code: str, imported_libraries: Optional[Set] = None
    ) -> Set[str]:
        """Import required libraries based on the generated code.

        Will look for any libraries that are not already imported (within sys.modules)
        and import them.

        :param code: The code to analyze for imports.
        :param imported_libraries: A set of libraries that have already been imported.
        :return: A set of imported libraries.
        """
        importer = cls(imported_libraries=imported_libraries or set())
        importer._import_required_libraries(code)

        return importer.imported_libraries

    def _import_required_libraries(self, code: str, dry_run: bool = False) -> None:
        """
        Import required libraries based on the generated code.

        :param code: The code to analyze for imports.
        """
        libraries = self._extract_libraries(code)

        self._log_code(libraries, "Libraries to import:")

        if dry_run:
            return

        self._import_libraries(libraries)
        self._log_code(self.imported_libraries, "Imported libraries:")

    def _extract_libraries(self, code: str) -> Set[str]:
        """
        Extract library names from the code using flake8.

        :param code: The code to analyze.
        :return: A set of library names.
        """
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        try:
            flake8_result = self._run_flake8(temp_file_path)
            return self._parse_flake8_output(flake8_result)
        finally:
            os.unlink(temp_file_path)

    def _run_flake8(self, file_path: str) -> str:
        """
        Run flake8 on the given file.

        :param file_path: Path to the file to analyze.
        :return: The stdout from flake8.
        """
        try:
            result = subprocess.run(
                ["flake8", "--select=F401", file_path],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Flake8 failed with error: {e}")
            return ""

    def _parse_flake8_output(self, output: str) -> Set[str]:
        """
        Parse flake8 output to extract library names.

        :param output: The flake8 output to parse.
        :return: A set of library names.
        """
        libraries = set()
        for line in output.splitlines():
            parts = line.split("'")
            if len(parts) >= 2:
                lib = parts[1].split(".")[0]
                libraries.add(lib)
        return libraries

    def _import_libraries(self, libraries: Set[str]) -> None:
        """
        Import the given libraries if they're not already imported.

        :param libraries: Set of library names to import.
        """
        for lib in libraries:
            if lib not in sys.modules and lib not in self.imported_libraries:
                try:
                    importlib.import_module(lib)
                    self.imported_libraries.add(lib)
                    print(f"Imported {lib}")
                except ImportError as e:
                    print(f"Failed to import {lib}: {e}")
