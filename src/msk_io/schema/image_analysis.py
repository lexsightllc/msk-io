# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import Field

from msk_io.schema._pydantic_base import MSKIOBaseModel
from msk_io.schema.dicom_data import DICOMVolume


class ImageMetaData(MSKIOBaseModel):
    """Basic metadata for a processed image."""

    original_path: str
    processed_path: str | None = None
    image_format: str  # e.g., 'png', 'nifti', 'dcm'
    dimensions: list[int]  # e.g., [H, W] or [D, H, W]
    channels: int | None = None
    voxel_spacing: list[float] | None = None  # for 3D volumes


class RegionOfInterest(MSKIOBaseModel):
    """Defines a region of interest within an image or volume."""

    roi_id: str
    label: str  # e.g., 'Kidney', 'Tumor', 'Liver'
    bounding_box_2d: list[int] | None = None
    bounding_box_3d: list[int] | None = None
    centroid_2d: list[float] | None = None
    centroid_3d: list[float] | None = None
    volume_mm3: float | None = None
    area_mm2: float | None = None
    pixel_count: int | None = None
    mask_file_path: str | None = None
    confidence_score: float | None = None
    segmentation_model_used: str | None = None


class ImageSegmentationResult(MSKIOBaseModel):
    """Result of an image segmentation operation."""

    source_volume: DICOMVolume
    segmentation_id: str
    segmented_at: datetime = Field(default_factory=datetime.now)
    regions_of_interest: list[RegionOfInterest]
    segmentation_method: str
    processed_image_meta: ImageMetaData


class ImageFeature(MSKIOBaseModel):
    """A generic feature extracted from an image or ROI."""

    feature_name: str
    value: Any
    unit: str | None = None
    description: str | None = None
    method_used: str | None = None


class ImageAnalysisResult(MSKIOBaseModel):
    """Comprehensive result of an image analysis, including segmentation and features."""

    analysis_id: str = Field(default_factory=lambda: str(uuid4()))
    analyzed_volume: DICOMVolume
    segmentation_results: list[ImageSegmentationResult] = Field(default_factory=list)
    extracted_features: list[ImageFeature] = Field(default_factory=list)
    qualitative_observations: str | None = None
    analysis_time: datetime = Field(default_factory=datetime.now)
    status: Literal["SUCCESS", "FAILURE", "PARTIAL_SUCCESS"] = "SUCCESS"
    errors: list[dict[str, Any]] = Field(default_factory=list)

    def add_segmentation(self, seg_result: ImageSegmentationResult) -> None:
        self.segmentation_results.append(seg_result)

    def add_feature(self, feature: ImageFeature) -> None:
        self.extracted_features.append(feature)
