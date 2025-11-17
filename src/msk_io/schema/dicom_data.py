# SPDX-License-Identifier: MPL-2.0
from datetime import date, time
from typing import Any

from pydantic import Field

from msk_io.schema._pydantic_base import MSKIOBaseModel


class DICOMPatientInfo(MSKIOBaseModel):
    """Information pertaining to the patient from DICOM metadata."""

    patient_id: str
    patient_name: str
    patient_sex: str | None = None
    patient_birth_date: date | None = None
    patient_age: str | None = None  # e.g., '060Y'
    other_patient_ids: list[str] = Field(default_factory=list)


class DICOMStudyInfo(MSKIOBaseModel):
    """Information pertaining to a DICOM study."""

    study_instance_uid: str
    study_id: str
    study_description: str | None = None
    study_date: date | None = None
    study_time: time | None = None
    accession_number: str | None = None
    referring_physician_name: str | None = None


class DICOMSeriesInfo(MSKIOBaseModel):
    """Information pertaining to a DICOM series."""

    series_instance_uid: str
    series_number: int | None = None
    series_description: str | None = None
    modality: str
    body_part_examined: str | None = None
    protocol_name: str | None = None


class DICOMImageInfo(MSKIOBaseModel):
    """Metadata specific to a single DICOM image slice or volume."""

    sop_instance_uid: str
    instance_number: int | None = None
    pixel_spacing: list[float] | None = None
    slice_thickness: float | None = None
    image_orientation_patient: list[float] | None = None
    image_position_patient: list[float] | None = None
    rows: int
    columns: int
    bits_allocated: int
    bits_stored: int
    high_bit: int
    pixel_representation: int  # 0 for unsigned, 1 for signed
    window_center: float | None = None
    window_width: float | None = None
    rescale_intercept: float | None = None
    rescale_slope: float | None = None
    photometric_interpretation: str
    transfer_syntax_uid: str


class DICOMVolume(MSKIOBaseModel):
    """Represents a 3D medical image volume derived from DICOM series."""

    series_instance_uid: str
    dicom_files: list[str]
    volume_path: str
    original_modality: str
    patient_info: DICOMPatientInfo
    study_info: DICOMStudyInfo
    series_info: DICOMSeriesInfo
    volume_shape: list[int]
    voxel_spacing: list[float]


class DICOMData(MSKIOBaseModel):
    """Aggregated DICOM data, potentially including multiple studies or volumes."""

    raw_dicom_paths: list[str]
    patient_info: DICOMPatientInfo
    studies: list[DICOMStudyInfo]
    series_volumes: list[DICOMVolume]
    all_raw_metadata: list[dict[str, Any]] = Field(default_factory=list)
