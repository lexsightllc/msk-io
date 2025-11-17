# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import Field

from msk_io.schema._pydantic_base import MSKIOBaseModel


class Metric(MSKIOBaseModel):
    """A single evaluation metric."""

    name: str
    value: float
    unit: str | None = None
    description: str | None = None


class EvaluationReport(MSKIOBaseModel):
    """A comprehensive report of an evaluation run."""

    report_id: str = Field(default_factory=lambda: str(uuid4()))
    evaluation_target: str
    evaluated_entity_id: str | None = None
    timestamp: datetime = Field(default_factory=datetime.now)
    metrics: list[Metric] = Field(default_factory=list)
    dataset_info: dict[str, Any] = Field(default_factory=dict)
    configuration_used: dict[str, Any] = Field(default_factory=dict)
    qualitative_observations: str | None = None
    recommendations: list[str] = Field(default_factory=list)
    status: Literal["PASSED", "FAILED", "IN_PROGRESS", "N/A"] = "N/A"
    errors: list[dict[str, Any]] = Field(default_factory=list)

    def add_metric(self, metric: Metric) -> None:
        self.metrics.append(metric)

    def add_metrics(self, metrics: list[Metric]) -> None:
        self.metrics.extend(metrics)
