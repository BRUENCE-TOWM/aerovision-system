from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.conf import settings
from django.utils import timezone

from .models import UploadAsset


def serialize_upload(upload: UploadAsset) -> dict[str, Any]:
    # All upload-facing JSON responses use this shape so template pages and
    # future frontend clients stay aligned.
    return {
        "id": upload.id,
        "title": upload.title,
        "description": upload.description,
        "file_url": upload.asset.url if upload.asset else "",
        "file_name": upload.asset.name if upload.asset else "",
        "status": upload.status,
        "status_label": upload.get_status_display(),
        "yolo_status": upload.yolo_status,
        "yolo_status_label": upload.get_yolo_status_display(),
        "yolo_model_name": upload.yolo_model_name,
        "yolo_result": upload.yolo_result,
        "analyzed_at": upload.analyzed_at.isoformat() if upload.analyzed_at else None,
        "created_at": upload.created_at.isoformat(),
        "updated_at": upload.updated_at.isoformat(),
    }


@dataclass
class YoloPredictionResult:
    model_name: str
    status: str
    detections: list[dict[str, Any]]
    raw: dict[str, Any]


class BaseYoloGateway:
    def predict(self, upload: UploadAsset) -> YoloPredictionResult:
        raise NotImplementedError


class StubYoloGateway(BaseYoloGateway):
    """Minimal placeholder gateway for later replacement with a real YOLO pipeline."""

    def predict(self, upload: UploadAsset) -> YoloPredictionResult:
        model_name = getattr(settings, "YOLO_DEFAULT_MODEL", "yolo-placeholder")
        raw = {
            "message": "YOLO gateway stub executed successfully.",
            "asset_name": upload.asset.name if upload.asset else "",
            "asset_path": upload.asset.path if upload.asset else "",
        }
        detections = [
            {
                "label": "placeholder-object",
                "confidence": 0.0,
                "bbox": [0, 0, 0, 0],
            }
        ]
        return YoloPredictionResult(
            model_name=model_name,
            status=UploadAsset.YOLO_STATUS_DONE,
            detections=detections,
            raw=raw,
        )


def get_yolo_gateway() -> BaseYoloGateway:
    # The gateway lookup is isolated here so the stub can later be replaced by
    # a real YOLO client without changing callers.
    return StubYoloGateway()


def run_yolo_prediction(upload: UploadAsset) -> UploadAsset:
    gateway = get_yolo_gateway()
    # Persist the transition to a queued state before invoking the model layer.
    upload.yolo_status = UploadAsset.YOLO_STATUS_QUEUED
    upload.save(update_fields=["yolo_status", "updated_at"])

    try:
        result = gateway.predict(upload)
    except Exception as exc:
        # Store failure details on the upload itself so the frontend can render
        # a meaningful error state without extra log access.
        upload.yolo_status = UploadAsset.YOLO_STATUS_FAILED
        upload.yolo_result = {"error": str(exc)}
        upload.analyzed_at = timezone.now()
        upload.save(update_fields=["yolo_status", "yolo_result", "analyzed_at", "updated_at"])
        raise

    upload.yolo_status = result.status
    upload.yolo_model_name = result.model_name
    upload.yolo_result = {
        "detections": result.detections,
        "raw": result.raw,
    }
    # The stored result is intentionally normalized even if the underlying
    # model provider returns a different raw schema.
    upload.analyzed_at = timezone.now()
    upload.save(
        update_fields=["yolo_status", "yolo_model_name", "yolo_result", "analyzed_at", "updated_at"]
    )
    return upload
