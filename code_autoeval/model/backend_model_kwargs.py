"""Backend model kwargs validation."""

from typing import TypedDict


class BackendModelKwargs(TypedDict, total=False):
    temperature: float
    max_tokens: int
    top_p: float
    frequency_penalty: float
    presence_penalty: float
