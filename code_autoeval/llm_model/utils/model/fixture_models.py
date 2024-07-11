import ast
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class FixtureInfo(BaseModel):
    module_path: Path
    fixture_name: str
    imported_class_name: str
    fixture_class_name: str  # Likely MagicMock -- only keeping for more context
    fixture_ast: Optional[ast.FunctionDef] = None
    imported_class_ast: Optional[ast.ClassDef] = None

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self) -> str:
        return f"""
        FixtureInfo(
            module_path={self.module_path},
            fixture_name={self.fixture_name},
            imported_class_name={self.imported_class_name},
            fixture_class_name={self.fixture_class_name},
            fixture_ast={self.fixture_ast},
            imported_class_ast={self.imported_class_ast}
        )
        """


class ClassFixtures(BaseModel):
    class_name: str
    fixtures: list[FixtureInfo]
