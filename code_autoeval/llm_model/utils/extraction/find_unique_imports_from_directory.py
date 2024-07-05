"""FInd unique imports from a directory"""

from pathlib import Path
from pprint import pprint
from typing import Dict, List

from multiuse.filepaths.find_project_root import FindProjectRoot
from tqdm import tqdm

from code_autoeval.llm_model.utils.extraction import extract_imports_from_file


class FindUniqueImportsFromDirectory:
    """Find the unique imports from a directory."""

    @classmethod
    def find_unique_imports_from_dir(
        cls, subdirectory_name: str = "code_autoeval", verbose: bool = False
    ) -> dict:
        instance = cls()
        files = instance._find_all_candidate_files(subdirectory_name, verbose)
        extracted_imports = instance._find_all_extracted_imports(files)
        return instance._find_unique_extracted_imports(extracted_imports)

    def _find_all_candidate_files(
        self, subdirectory_name: str = "code_autoeval", verbose: bool = False
    ) -> List[Path]:
        """Find all candidate files."""
        # Find the projeft root
        project_root = FindProjectRoot.find_project_root()
        files = list(project_root.joinpath(subdirectory_name).rglob("*.py"))

        if verbose:
            print(f"Found {len(files)} files.")

        return files

    def _find_all_extracted_imports(self, files: list) -> list[dict]:
        extracted_imports = []

        extract_imports = extract_imports_from_file.ExtractImportsFromFile()

        for f in tqdm(files):

            if f.name == "__init__.py":
                continue

            file_contents = f.read_text()

            extracted_from_file = extract_imports.extract_imports(file_contents)

            pprint(extracted_from_file)

            extracted_imports.append(extracted_from_file)

        return extracted_imports

    def _find_unique_extracted_imports(self, extracted_imports: list[dict]) -> dict:
        unique_imports: Dict[str, str] = {}
        for d in extracted_imports:
            unique_imports |= d

        return unique_imports
