# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import Field

from msk_io.schema._pydantic_base import MSKIOBaseModel


class ServiceHealth(MSKIOBaseModel):
    """Provides health status of an internal service or component."""

    service_name: str
    is_healthy: bool
    status_message: str
    last_checked: datetime = Field(default_factory=datetime.now)
    details: dict[str, Any] | None = None


class SystemHealthReport(MSKIOBaseModel):
    """Overall system health report for the MSK-IO pipeline."""

    report_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    overall_status: Literal["OPERATIONAL", "DEGRADED", "OUTAGE"]
    message: str | None = None
    service_statuses: list[ServiceHealth] = Field(default_factory=list)


class RuntimeMetrics(MSKIOBaseModel):
    """Runtime performance metrics for a specific operation."""

    operation_name: str
    duration_seconds: float
    cpu_usage_percent: float | None = None
    memory_usage_mb: float | None = None
    disk_io_mb_per_s: float | None = None
    network_io_mb_per_s: float | None = None
