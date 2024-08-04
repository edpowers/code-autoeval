"""Base class."""

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import find_dotenv, load_dotenv
from multiuse.filepaths.find_project_root import FindProjectRoot
from pydantic import BaseModel, Field

__all__ = [
    "BaseModelConfig",
    "LLMModelAttributes",
    "CommonAttributes",
    "ModelAttributesFactory",
    "CommonAttributesFactory",
    "InitKwargs",
    "BaseLLMClass",
]


class BaseModelConfig(BaseModel):
    """Base model configuration."""

    class Config:
        arbitrary_types_allowed = True


class LLMModelAttributes(BaseModel):
    """Model attributes."""

    llm_model_name: str = ""
    llm_model_url: str = ""


class CommonAttributes(BaseModelConfig):
    """Common attributes for all classes."""

    project_root: Path
    generated_base_dir: Path
    generated_base_log_dir: Path  # For storing logs in each of the functions.
    class_logger: logging.Logger


class ModelAttributesFactory(BaseModel):
    """Factory for creating ModelAttributes with default values."""

    @staticmethod
    def create() -> LLMModelAttributes:
        load_dotenv(find_dotenv())
        return LLMModelAttributes(
            llm_model_name=os.getenv("OPENAI_MODEL_NAME", "coder-lite:latest"),
            llm_model_url=os.getenv("OPENAI_BASE_URL", ""),
        )


class CommonAttributesFactory(BaseModel):
    """Factory for creating CommonAttributes with default values."""

    @staticmethod
    def create() -> CommonAttributes:
        project_root = FindProjectRoot().find_project_root()
        assert isinstance(project_root, Path)
        assert project_root.exists()

        generated_base_dir = project_root.joinpath("generated_code")
        generated_base_log_dir = project_root.joinpath("generated_code_logs")
        return CommonAttributes(
            project_root=project_root,
            generated_base_dir=generated_base_dir,
            generated_base_log_dir=generated_base_log_dir,
            class_logger=logging.getLogger(__name__),
        )


class InitKwargs(BaseModel):

    verbose: bool
    debug: bool
    func_name: str


class BaseLLMClass(BaseModelConfig):
    """Base class."""

    coverage_result: Any = None  # subprocess completed process
    file_path: Optional[Path] = None
    test_file_path: Optional[Path] = None
    absolute_path_from_root: Optional[Path] = None

    common: CommonAttributes = Field(default_factory=CommonAttributesFactory.create)

    unique_imports_dict: Dict[str, str] = {}  # Modifiable.

    init_kwargs: InitKwargs = Field(
        default_factory=lambda: InitKwargs(verbose=False, debug=False, func_name="")
    )
    llm_model_attributes: LLMModelAttributes = Field(
        default_factory=ModelAttributesFactory.create
    )

    def __init___(self, **kwargs: InitKwargs) -> None:
        super().__init__(**kwargs)
