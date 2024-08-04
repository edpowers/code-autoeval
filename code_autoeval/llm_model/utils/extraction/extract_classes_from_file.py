"""Extract (and remove) specific classes within a file."""

import ast
import shutil
import tempfile
from pathlib import Path
from pprint import pprint
from typing import List, Optional, Tuple


class PythonClassManager:
    def __init__(self, file_path: str = "", content: str = ""):
        """
        Initialize the PythonClassManager.

        Args:
        file_path (str): The path to the Python file to analyze and modify.
        """
        self.is_temp_file = False

        if (
            file_path
            and isinstance(file_path, str)
            and not Path(file_path).exists()
            and content
        ):
            print(
                f"PythonClassManager - Creating a new file at {file_path} with the provided content."
            )
            # Then create the actual file. Easier to do this here than in the constructor
            with open(file_path, "w") as file:
                file.write(content)
        elif not file_path:
            if not content:
                raise ValueError("Either file_path or content must be provided.")

            print(
                "PythonClassManager - No file path provided, so creating a temporary file from valid content."
            )

            # Then assume that no valid file path was passed in
            # so we should make a temporary file
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
                temp_file.write(content)
                file_path = temp_file.name
                # Mark the is_temp_file flag as True
                self.is_temp_file = True

        if not content and file_path:
            with open(file_path, "r") as file:
                content = file.read()

        if not content:
            raise ValueError("The content is empty - and the file is empty.")

        self.file_path = file_path
        self.content = content

    @classmethod
    def extract_remove_class_from_file(
        cls,
        name_of_class_to_remove: str,
        file_path: str = "",
        content: str = "",
    ) -> str:
        manager = PythonClassManager(file_path, content=content)

        # If the class to remove is not in the content, then return the content as is
        if name_of_class_to_remove not in manager.content:
            return manager.content

        class_definitions: List[Tuple[str, int, int]] = manager.find_class_definitions()

        # If there are no class definitions, then return the content as is
        if not class_definitions:
            return manager.content

        if name_of_class_to_remove in [str(cls) for cls, _, _ in class_definitions]:
            manager.remove_classes(name_of_class_to_remove)

        try:
            removed_classes = manager.remove_classes(name_of_class_to_remove)
            successfully_removed, remaining_classes = manager.verify_class_removal(
                removed_classes
            )

            if successfully_removed:
                print(f"\nSuccessfully removed the following classes from {file_path}:")
                for cls in successfully_removed:
                    print(f"  - {cls}")
            else:
                print(f"\nNo classes were removed from {file_path}")

            if remaining_classes:
                print("\nRemaining classes in the file:")
                for cls, start, end in remaining_classes:
                    print(f"  - {cls} (lines {start}-{end})")
            else:
                print("\nNo classes remain in the file.")

        except (FileNotFoundError, SyntaxError) as e:
            print(f"Error: {str(e)}")

        # Then read the file path back into the content
        with open(file_path, "r") as f:
            content = f.read()

        # If this was a temporary file, then remove it
        if manager.is_temp_file:
            Path(file_path).unlink(missing_ok=True)
        if not content:
            raise ValueError("The content is empty.")

        return content

    def find_class_definitions(self) -> List[Tuple[str, int, int]]:
        """
        Find all class definitions in the Python file.

        Returns:
        List[Tuple[str, int, int]]: A list of tuples, each containing the class name,
                                    its start line number, and its end line number.

        Raises:
        FileNotFoundError: If the specified file does not exist.
        SyntaxError: If the file contains invalid Python syntax.
        """
        try:
            with open(self.file_path, "r") as file:
                content = file.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {self.file_path} does not exist.") from e

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            pprint(content)
            raise SyntaxError(
                f"Invalid Python syntax in {self.file_path}: {str(e)}"
            ) from e

        class_definitions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                start_line = node.lineno
                end_line = max(
                    getattr(node, "end_lineno", node.lineno),
                    max(
                        (
                            getattr(child, "end_lineno", child.lineno)
                            for child in ast.iter_child_nodes(node)
                        ),
                        default=node.lineno,
                    ),
                )

                # Read in the lines of the class definition
                lines_from_extracted = self.content.splitlines()[
                    start_line - 1 : end_line
                ]

                # Check if the class definition contains any MagicMock, patch, or other
                # unittest.mock related imports
                if any(
                    "unittest.mock" in line or "MagicMock" in line or "patch" in line
                    for line in lines_from_extracted
                ):
                    return []

                class_definitions.append((node.name, start_line, end_line))

        return class_definitions

    def remove_classes(self, class_to_remove: Optional[str] = None) -> List[str]:
        """
        Remove specified class definitions from the file.

        Args:
        class_to_remove (Optional[str]): The name of a specific class to remove. If None, remove all classes.

        Returns:
        List[str]: A list of class names that were successfully removed.

        Raises:
        FileNotFoundError: If the specified file does not exist.
        SyntaxError: If the file contains invalid Python syntax.
        """
        initial_classes = self.find_class_definitions()
        classes_to_remove = [
            cls
            for cls, _, _ in initial_classes
            if class_to_remove is None or cls == class_to_remove
        ]

        with open(self.file_path, "r") as file:
            lines = file.readlines()

            if not lines:
                raise ValueError("The file is empty.")

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            skip_lines = set()
            for cls, start, end in initial_classes:
                if cls in classes_to_remove:
                    skip_lines.update(range(start, end + 1))

            for i, line in enumerate(lines, 1):
                if i not in skip_lines:
                    temp_file.write(line)

        shutil.move(temp_file.name, self.file_path)

        remaining_classes = self.find_class_definitions()
        remaining_class_names = [cls for cls, _, _ in remaining_classes]

        return [cls for cls in classes_to_remove if cls not in remaining_class_names]

    def verify_class_removal(
        self, removed_classes: List[str]
    ) -> Tuple[List[str], List[Tuple[str, int, int]]]:
        """
        Verify the removal of classes and return remaining classes.

        Args:
        removed_classes (List[str]): List of class names that were supposed to be removed.

        Returns:
        Tuple[List[str], List[Tuple[str, int, int]]]: A tuple containing:
            - List of class names that were successfully removed.
            - List of remaining class definitions (name, start line, end line).
        """
        remaining_classes = self.find_class_definitions()
        remaining_class_names = [cls for cls, _, _ in remaining_classes]
        successfully_removed = [
            cls for cls in removed_classes if cls not in remaining_class_names
        ]
        return successfully_removed, remaining_classes
