# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import Field

from msk_io.schema._pydantic_base import MSKIOBaseModel


class DataSource(MSKIOBaseModel):
    """Information about a data source from which medical data was retrieved."""

    source_id: str
    source_type: Literal[
        "DICOM_PACS", "OHIF_Viewer", "Local_Filesystem", "Cloud_Storage"
    ]
    endpoint_url: str | None = None
    access_method: str | None = None
    last_accessed: datetime | None = None


class RetrievedDataInfo(MSKIOBaseModel):
    """Summary of data retrieved for a specific processing run."""

    retrieval_id: str = Field(default_factory=lambda: str(uuid4()))
    data_source: DataSource
    original_query: str | None = None
    retrieved_file_paths: list[str] = Field(default_factory=list)
    total_files_retrieved: int
    total_size_bytes: int | None = None
    retrieval_start_time: datetime = Field(default_factory=datetime.now)
    retrieval_end_time: datetime = Field(default_factory=datetime.now)
    status: Literal["SUCCESS", "FAILURE", "PARTIAL_SUCCESS"] = "SUCCESS"
    message: str | None = None
    errors: list[dict[str, Any]] = Field(default_factory=list)
    series_volumes: list[Any] = Field(default_factory=list)
