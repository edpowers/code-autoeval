"""Model the class data getting passed into generate code."""

import importlib
import inspect
from pathlib import Path
from typing import Any, Dict, List, Tuple

from multiuse.filepaths.system_utils import SystemUtils
from pydantic import Field

from code_autoeval.llm_model.utils.model.pretty_print_base_model import (
    PrettyPrintBaseModel,
)


class ClassDataModel(PrettyPrintBaseModel):
    """Class data."""

    class_object: object  # The actual class object
    class_name: str  # The name of the class
    class_methods: List[str]  # The methods (functions) of the class
    class_attributes: List[str]  # The attributes of the class
    init_params: List[str]  # The parameters of the __init__ method
    base_classes: List[str]  # The base classes of the class
    absolute_path: str  # The absolute path to the class file - full path on host system
    coroutine_methods: List[str]  # The coroutine methods of the class

    module_absolute_path: Path = Field(
        None, description="Absolute path to the module file"
    )
    module_relative_path: Path = Field(
        None, description="Relative path from the project root to the module file"
    )


class ClassDataModelFactory:

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def create_from_class_info(
        self, class_info: Dict[str, List[Tuple[str, str, List[str]]]]
    ) -> List[ClassDataModel]:
        class_data_models = []

        for file_path, classes in class_info.items():
            for class_name, import_path, function_names in classes:
                if not function_names:
                    print(f"Skipping: No functions to implement for {classes}")
                    continue

                print(f"Generating code for class: {class_name} from {file_path}")

                try:
                    class_to_process = self._import_class(import_path)

                    # Get the absolute path of the function's module
                    module_path = Path(
                        SystemUtils.get_class_file_path(class_to_process)
                    )
                    # Create the relative path from the project root
                    relative_path = module_path.relative_to(self.project_root)

                    class_model = ClassDataModel(
                        class_object=class_to_process,
                        class_name=class_name,
                        class_methods=function_names,
                        class_attributes=ClassDataModelFactory._get_class_attributes(
                            class_to_process
                        ),
                        init_params=ClassDataModelFactory._get_init_parameters(
                            class_to_process
                        ),
                        base_classes=ClassDataModelFactory._get_base_classes(
                            class_to_process
                        ),
                        absolute_path=import_path,
                        coroutine_methods=ClassDataModelFactory._get_coroutine_methods(
                            class_to_process
                        ),
                        module_absolute_path=module_path,
                        module_relative_path=relative_path,
                    )

                    class_data_models.append(class_model)

                except Exception as e:
                    print(f"Error processing class {class_name}: {str(e)}")

        return class_data_models

    @staticmethod
    def _import_class(import_path: str) -> Any:
        module_name, class_name = import_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    @staticmethod
    def _get_base_classes(class_to_process: Any) -> List[str]:
        return [base.__name__ for base in class_to_process.__bases__]

    @staticmethod
    def _get_class_attributes(class_to_process: Any) -> List[str]:
        return [
            name
            for name in dir(class_to_process)
            if not name.startswith("__")
            and not callable(getattr(class_to_process, name))
        ]

    @staticmethod
    def _get_init_parameters(class_to_process: Any) -> List[str]:
        init_signature = inspect.signature(class_to_process.__init__)
        return [
            param.name
            for param in init_signature.parameters.values()
            if param.name != "self"
        ]

    @staticmethod
    def _get_coroutine_methods(class_to_process: Any) -> List[str]:
        return [
            name
            for name, method in inspect.getmembers(class_to_process)
            if inspect.iscoroutinefunction(method) or inspect.isasyncgenfunction(method)
        ]
