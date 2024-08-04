import json
import os

import requests
from dotenv import find_dotenv, load_dotenv
from multiuse.filepaths.find_project_root import FindProjectRoot
from pydantic import BaseModel, computed_field

project_root = FindProjectRoot.find_project_root()

load_dotenv(find_dotenv(raise_error_if_not_found=True))

OPENAI_BASE_URL = os.env["OPENAI_BASE_URL"]


class ModelFileParams(BaseModel):
    huggingface_repo: str
    local_gguf_file: str
    temperature: float = 0.4
    top_k: int = 40
    top_p: float = 0.4
    repeat_penalty: float = 1.1

    def create_model_file(self):
        return f"""
FROM {self.huggingface_repo}/{self.local_gguf_file}

PARAMETER temperature {self.temperature}
PARAMETER top_k {self.top_k}
PARAMETER top_p {self.top_p}
PARAMETER repeat_penalty {self.repeat_penalty}
"""


class OllamaURLs(BaseModel):

    @computed_field  # type: ignore[misc]
    @property
    def base_url(self) -> str:
        return OPENAI_BASE_URL

    @computed_field  # type: ignore[misc]
    @property
    def create_model(self) -> str:
        return f"{self.base_url}/api/create"

    @computed_field  # type: ignore[misc]
    @property
    def generate(self) -> str:
        return f"{self.base_url}/api/generate"


def create_and_run_model(model_name: str, huggingface_repo: str, gguf_file: str):

    # Ollama API endpoint
    ollama_urls = OllamaURLs()
    # Modelfile content
    modelfile_params = ModelFileParams(
        huggingface_repo=huggingface_repo, local_gguf_file=gguf_file
    )
    modelfile = modelfile_params.create_model_file()

    # Request payload
    payload = {"name": model_name, "modelfile": modelfile}

    # Send POST request to create the model
    response = requests.post(url=ollama_urls.create_model, json=payload)

    if response.status_code == 200:
        print(f"Model '{model_name}' created successfully.")

        run_payload = {"model": model_name, "prompt": "Hello, how are you?"}

        run_response = requests.post(
            ollama_urls.generate, json=run_payload, stream=True
        )

        for line in run_response.iter_lines():
            if line:
                response_data = json.loads(line)
                if "response" in response_data:
                    print(response_data["response"], end="")
                if response_data.get("done", False):
                    print("\nGeneration complete.")
    else:
        print(f"Failed to create model. Status code: {response.status_code}")
        print(response.text)


# Usage
create_and_run_model(
    "my-llama-model", "TheBloke/Llama-2-7B-Chat-GGUF", "llama-2-7b-chat.Q4_K_M.gguf"
)
