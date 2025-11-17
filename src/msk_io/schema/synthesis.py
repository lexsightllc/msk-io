# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import Field

from msk_io.schema._pydantic_base import MSKIOBaseModel
from msk_io.schema.image_analysis import ImageAnalysisResult
from msk_io.schema.llm_output import DiagnosticFinding, LLMAnalysisResult
from msk_io.schema.retrieval_info import RetrievedDataInfo


class MultiModalInput(MSKIOBaseModel):
    """Aggregated input from various modalities for synthesis."""

    text_data: str | None = None
    image_analysis_results: list[ImageAnalysisResult] = Field(default_factory=list)
    llm_analysis_results: list[LLMAnalysisResult] = Field(default_factory=list)
    retrieved_data_info: RetrievedDataInfo | None = None


class MultiModalSynthesisResult(MSKIOBaseModel):
    """The result of synthesizing information from multiple modalities."""

    synthesis_id: str = Field(default_factory=lambda: str(uuid4()))
    input_data: MultiModalInput
    synthesized_conclusion: str
    supporting_findings: list[DiagnosticFinding] = Field(default_factory=list)
    consistency_score: float | None = None
    identified_discrepancies: list[str] = Field(default_factory=list)
    synthesized_at: datetime = Field(default_factory=datetime.now)
    status: Literal["SUCCESS", "FAILURE", "PARTIAL_SUCCESS"] = "SUCCESS"
    errors: list[dict[str, Any]] = Field(default_factory=list)

    def add_finding(self, finding: DiagnosticFinding) -> None:
        self.supporting_findings.append(finding)
