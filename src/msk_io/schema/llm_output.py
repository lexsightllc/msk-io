# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import Field

from msk_io.schema._pydantic_base import MSKIOBaseModel


class LLMInput(MSKIOBaseModel):
    """Represents the structured input provided to an LLM."""

    prompt_text: str
    context_data: dict[str, Any] = Field(default_factory=dict)
    model_name: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None


class LLMResponseChoice(MSKIOBaseModel):
    """A single choice from an LLM response."""

    text: str
    index: int
    logprobs: float | None = None
    finish_reason: str | None = None


class LLMOutput(MSKIOBaseModel):
    """Represents the structured output received from an LLM."""

    response_id: str
    model_name_used: str
    timestamp: datetime = Field(default_factory=datetime.now)
    input_tokens: int
    output_tokens: int
    total_tokens: int
    choices: list[LLMResponseChoice]
    raw_response: dict[str, Any] = Field(default_factory=dict)


class DiagnosticFinding(MSKIOBaseModel):
    """A specific diagnostic finding or observation from LLM analysis."""

    finding_id: str = Field(default_factory=lambda: str(uuid4()))
    category: str
    description: str
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW", "NORMAL"]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    associated_roi_ids: list[str] = Field(default_factory=list)
    supporting_evidence_texts: list[str] = Field(default_factory=list)
    recommended_action: str | None = None


class LLMAnalysisResult(MSKIOBaseModel):
    """Result of an LLM-based diagnostic analysis."""

    analysis_id: str = Field(default_factory=lambda: str(uuid4()))
    llm_output: LLMOutput
    extracted_findings: list[DiagnosticFinding]
    summary: str
    status: Literal["SUCCESS", "FAILURE", "PARTIAL_SUCCESS"] = "SUCCESS"
    errors: list[dict[str, Any]] = Field(default_factory=list)

    def add_finding(self, finding: DiagnosticFinding) -> None:
        self.extracted_findings.append(finding)
