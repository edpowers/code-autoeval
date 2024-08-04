"""Generate Fake Data."""

import asyncio
import random
import re
from typing import Any, Callable, Optional

import pandas as pd
from faker import Faker

from code_autoeval.llm_model.utils.model_response.stream_response import StreamResponse
from code_autoeval.llm_model.utils.preprocess_code_before_exec import (
    PreProcessCodeBeforeExec,
)
from code_autoeval.llm_model.utils.prompting.system_prompts import SystemPrompts


class GenerateFakeData(StreamResponse, PreProcessCodeBeforeExec, SystemPrompts):
    """Generate the fake data."""

    # @persistent_cache
    def generate_fake_data(
        self,
        func: Callable[..., Any],
        df: Optional[pd.DataFrame] = None,
        debug: bool = False,
        skip_generate_fake_data: bool = False,
    ) -> pd.DataFrame:
        """
        Generate fake data based on the function signature if needed.
        """
        return asyncio.run(
            self.async_generate_fake_data(func, df, debug, skip_generate_fake_data)
        )

    async def async_generate_fake_data(
        self,
        func: Callable[..., Any],
        df: Optional[pd.DataFrame] = None,
        debug: bool = False,
        skip_generate_fake_data: bool = False,
    ) -> pd.DataFrame:
        """
        Generate fake data based on the function signature if needed.
        """
        if df is not None or skip_generate_fake_data:
            return df

        self.debug = debug

        fake_data_prompt = self.generate_fake_data_prompt(func)

        fake_data_response = await self.ask_backend_model(
            fake_data_prompt, system_prompt=""
        )

        content = self.figure_out_model_response(fake_data_response)

        # Extract the code part
        parts = re.split(
            r"[# ]{0,2}Expected Output:|### Expected Output:", content, maxsplit=1
        )

        code = parts[0].strip()
        code = self.run_preprocess_pipeline(code, code_type="")
        # Log the code
        self._log_code(code)

        try:
            # Set up the execution environment
            local_vars = {"pd": pd, "Faker": Faker, "random": random}

            # Execute the code
            exec(code, local_vars)

            # Retrieve the generated fake_data
            fake_data = local_vars.get("fake_data")

            if not isinstance(fake_data, pd.DataFrame):
                raise ValueError("The generated fake data is not a pandas DataFrame")

            self._log_fake_gen_data(fake_data)

            return fake_data

        except Exception as e:
            raise Exception(f"Error creating fake data: {str(e)}\nCode:\n{code}") from e
