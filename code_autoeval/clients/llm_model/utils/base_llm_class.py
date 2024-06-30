"""Base class."""

import os
from pathlib import Path
from typing import Any

from dotenv import find_dotenv, load_dotenv
from multiuse.filepaths.find_project_root import FindProjectRoot
from pydantic import BaseModel, Field


class LLMModelAttributes(BaseModel):
    """Model attributes."""

    llm_model_name: str = ""
    llm_model_url: str = ""


class CommonAttributes(BaseModel):
    """Common attributes for all classes."""

    project_root: Path
    generated_base_dir: Path


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
        return CommonAttributes(
            project_root=project_root, generated_base_dir=generated_base_dir
        )


class InitKwargs(BaseModel):

    verbose: bool
    debug: bool
    func_name: str


class BaseLLMClass(BaseModel):
    """Base class."""

    coverage_result: Any = None  # subprocess completed process
    file_path: Path | None = None
    test_file_path: Path | None = None
    absolute_path_from_root: Path | None = None

    common: CommonAttributes = Field(default_factory=CommonAttributesFactory.create)

    init_kwargs: InitKwargs = Field(
        default_factory=lambda: InitKwargs(verbose=False, debug=False, func_name="")
    )
    llm_model_attributes: LLMModelAttributes = Field(
        default_factory=ModelAttributesFactory.create
    )

    def __init___(self, **kwargs: InitKwargs) -> None:
        super().__init__(**kwargs)

    class Config:
        arbitrary_types_allowed = True
