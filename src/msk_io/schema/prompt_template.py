# SPDX-License-Identifier: MPL-2.0
from typing import Literal

from pydantic import Field

from msk_io.schema._pydantic_base import MSKIOBaseModel


class PromptParameter(MSKIOBaseModel):
    """Defines a parameter that can be used within a prompt template."""

    name: str
    description: str
    is_required: bool = True
    default_value: str | None = None
    example_value: str | None = None
    data_type: Literal["string", "number", "boolean", "list", "json"] = "string"


class PromptTemplate(MSKIOBaseModel):
    """Defines a reusable template for constructing LLM prompts."""

    template_name: str
    description: str
    template_string: str
    parameters: list[PromptParameter] = Field(default_factory=list)
    expected_output_format: str | None = None
    example_usage: str | None = None

    def format(self, **kwargs: str) -> str:
        """Formats the prompt template string with provided keyword arguments."""
        missing = [
            p.name for p in self.parameters if p.is_required and p.name not in kwargs
        ]
        if missing:
            raise ValueError(
                f"Missing required prompt parameters: {', '.join(missing)}"
            )
        return self.template_string.format(**kwargs)


class PromptSet(MSKIOBaseModel):
    """A collection of related prompt templates for a specific task or agent."""

    set_name: str
    description: str
    prompts: list[PromptTemplate]
