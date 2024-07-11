"""Execute the generated code."""

import re
from typing import Any, Dict, Optional, Tuple

import pandas as pd
from multiuse.model import class_data_model
from pydantic import Field

from code_autoeval.llm_model import imports
from code_autoeval.llm_model.utils import (
    extraction,
    model,
    model_response,
    preprocess_code_before_exec,
    validation,
)


class ExecuteGeneratedCode(
    model_response.SerializeDataframes,
    preprocess_code_before_exec.PreProcessCodeBeforeExec,
    extraction.FindParentClass,
    validation.ValidateRegexes,
    imports.ExtractImportsFromFile,
    imports.DynamicallyImportPackages,
):

    imported_libraries: set = Field(default_factory=set)

    global_imports: imports.GlobalImports = Field(default_factory=imports.GlobalImports)

    function_argument_finder: extraction.FunctionArgumentFinder = Field(
        default_factory=extraction.FunctionArgumentFinder
    )

    def execute_generated_code(
        self,
        original_code: str,
        func_attributes: model.FunctionAttributes,
        df: Optional[pd.DataFrame] = None,
        debug: bool = False,
        class_model: Optional[class_data_model.ClassDataModel] = None,
    ) -> Tuple[Any, Dict[str, Any]]:
        """
        Executes the generated Python code and returns the result and context.

        If the class model is provided, then return empty dictionaries and
        skip running the code.

        TODO: Add support for running existing code rather than skipping it.

        :param code: The code to execute
        :param func: The original function object
        :param df: Optional dataframe to use in code execution
        :param debug: Whether to print debug information
        :return: A tuple containing the result and the execution context
        """
        if class_model:
            return {}, {}

        # Create a new dictionary for local variables
        local_vars = {}
        # Add the input dataframe to the local variables if provided
        if isinstance(df, pd.DataFrame) and not df.empty:
            local_vars["df"] = df

        # Remove markdown code blocks if present
        code = self.remove_non_code_patterns(
            original_code, code_type="function", func_name=self.init_kwargs.func_name
        )

        self.global_imports = self.global_imports.create_global_imports()
        global_vars = self.global_imports.run_global_imports()

        # TODO: Test this.
        # Extract import statements
        import_dict = self.extract_imports(
            code, str(func_attributes.module_relative_path)
        )
        imports = "\n".join(list(import_dict.values()))
        # Log the value of the imports
        self._log_code(imports, "Extracted Imports:")

        # Execute imports separately
        exec(imports, global_vars)
        # Remove import statements from the main code
        main_code = re.sub(r"^(import|from) .*\n?", "", code, flags=re.MULTILINE)

        # Execute the code
        try:
            # Import required libraries
            imported_libs = self.import_required_libraries(main_code)

            # Find the target in the code
            target_node = self.find_target_in_code(
                main_code,
                func_attributes.method_name,
            )
            # Target source
            target_source, parent_class_name = self.find_and_extract_target(
                main_code, self.init_kwargs.func_name
            )

            self.validate_target_node(target_node, self.init_kwargs.func_name)

            exec(main_code, global_vars, local_vars)
            # Update local variable names to avoid conflicts
            local_vars = self.update_local_var_names(local_vars)

            if parent_class_name:
                self.validate_class_name_in_local_vars(parent_class_name, local_vars)

                parent_class = local_vars[parent_class_name]
                instance = parent_class()
                generated_func = getattr(instance, func_attributes.method_name)

                # Wrap the method to handle 'self' automatically
                def wrapped_method(*args, **kwargs):
                    return generated_func(*args, **kwargs)

                generated_func = wrapped_method
            else:
                # Let's also make sure that the split function is in the local_vars
                parts = self.init_kwargs.func_name.split(".") + [
                    self.init_kwargs.func_name
                ]
                if all(part not in local_vars for part in parts):
                    # If the function is not in local_vars, explicitly execute its source
                    exec(target_source, global_vars, local_vars)

                if len(parts) == 3:
                    # It's a method
                    class_name, method_name = parts[:2]
                    class_obj = local_vars[class_name]
                    generated_func = getattr(class_obj, method_name)
                else:
                    generated_func = local_vars[func_attributes.func_name]

            # Find the arguments for the generated function
            args = self.function_argument_finder.find_args(generated_func, df)
            # Call the function with the prepared arguments
            # Deserialize the result if it's a DataFrame
            result = self.deserialize_dataframe(generated_func(*args))

            # Get the context (all variables in the local scope)
            # Deserialize any DataFrames in the context
            context = {
                k: self.deserialize_dataframe(v)
                for k, v in local_vars.items()
                if not k.startswith("__") and k != "df"
            }

            return result, context

        except Exception as e:
            raise Exception(f"Error executing code: {str(e)}\n Code:\n {code}") from e
