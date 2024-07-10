"""FInd unique imports from a directory"""

from pathlib import Path
from pprint import pprint
from typing import Dict, List

from multiuse.filepaths.find_project_root import FindProjectRoot
from tqdm import tqdm

from code_autoeval.llm_model.utils.extraction import extract_imports_from_file


class FindImportsFromDir:
    """Find the unique imports from a directory."""

    project_root: Path

    @classmethod
    def find_unique_imports_from_dir(
        cls, subdirectory_name: str = "code_autoeval", verbose: bool = False
    ) -> dict:
        instance = cls()
        # Find the projeft root
        instance.project_root = FindProjectRoot.find_project_root()

        files = instance._find_all_candidate_files(subdirectory_name, verbose)
        extracted_imports = instance._find_all_extracted_imports(files, verbose)
        return instance._find_unique_extracted_imports(extracted_imports)

    def _find_all_candidate_files(
        self, subdirectory_name: str = "code_autoeval", verbose: bool = False
    ) -> List[Path]:
        """Find all candidate files."""
        files = list(self.project_root.joinpath(subdirectory_name).rglob("*.py"))

        if verbose:
            print(f"Found {len(files)} files.")

        return files

    def _find_all_extracted_imports(
        self, files: list, verbose: bool = False
    ) -> list[dict]:
        extracted_imports = []

        extract_imports = extract_imports_from_file.ExtractImportsFromFile()

        for f in tqdm(files):

            if f.name == "__init__.py":
                continue

            file_contents = f.read_text()

            # Relative path
            relative_fpath = (
                str(f.relative_to(self.project_root))
                .removesuffix(".py")
                .replace("/", ".")
            )

            extracted_from_file = extract_imports.extract_imports(
                file_contents, relative_fpath
            )

            if verbose:
                pprint(extracted_from_file)

            extracted_imports.append(extracted_from_file)

        return extracted_imports

    def _find_unique_extracted_imports(self, extracted_imports: list[dict]) -> dict:
        unique_imports: Dict[str, str] = {}
        for d in extracted_imports:
            unique_imports |= d

        # Now sort the dictionary by keys in alphabetical order
        unique_imports = dict(sorted(unique_imports.items()))

        return unique_imports
