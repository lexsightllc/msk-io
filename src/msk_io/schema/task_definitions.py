# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import Field

from msk_io.schema._pydantic_base import MSKIOBaseModel


class AgentInstruction(MSKIOBaseModel):
    """A specific instruction for an agent to perform."""

    instruction_id: str = Field(default_factory=lambda: str(uuid4()))
    command: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    target_agent: str | None = None
    priority: int = Field(0, ge=0, description="Higher value means higher priority.")


class AgentResponse(MSKIOBaseModel):
    """The response from an agent after executing an instruction."""

    response_id: str = Field(default_factory=lambda: str(uuid4()))
    instruction_id: str
    agent_name: str
    status: Literal["SUCCESS", "FAILED", "PENDING"]
    output_data: dict[str, Any] | None = None
    error_message: str | None = None
    timestamp: datetime = Field(default_factory=datetime.now)


class TaskDefinition(MSKIOBaseModel):
    """Defines a complex task composed of multiple agent instructions."""

    task_id: str = Field(default_factory=lambda: str(uuid4()))
    task_name: str
    description: str | None = None
    required_inputs: list[str] = Field(default_factory=list)
    output_type: str | None = None
    sequence_of_instructions: list[AgentInstruction] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
