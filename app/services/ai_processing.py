import time
from pathlib import Path
from typing import Any

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.repositories.mission import get_mission
from app.repositories.prediction_history import register_prediction_result
from app.schemas import InferenceRequest, InferenceResponse

MODEL_NAME = "aerial_mapping_yolo"
MODEL_VERSION = "1.0.0"
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".tif", ".tiff", ".geotiff"}
ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/tiff",
    "image/geotiff",
    "image/x-geotiff",
}


class ModelService:
    def __init__(self) -> None:
        self.model: dict[str, str] | None = None
        self.model_name = settings.ai_model_name or MODEL_NAME
        self.model_version = settings.ai_model_version or MODEL_VERSION

    def load_model(self) -> dict[str, str]:
        if self.model is None:
            self.model = {
                "name": self.model_name,
                "version": self.model_version,
            }
        return self.model

    def predict(self, image: Any) -> dict[str, Any]:
        self.load_model()

        start_time = time.perf_counter()
        result = {
            "detections": 17,
            "classes": {
                "building": 10,
                "road": 4,
                "vehicle": 3,
            },
        }
        inference_time = time.perf_counter() - start_time

        return {
            "model_name": self.model_name,
            "model_version": self.model_version,
            "inference_time": inference_time,
            "result": result,
        }


model_service = ModelService()


class AIProcessingService:
    def validate_image(self, image: UploadFile) -> bytes:
        if not image.filename:
            raise ValueError("Image filename is required")

        extension = Path(image.filename).suffix.lower()
        if extension not in ALLOWED_IMAGE_EXTENSIONS:
            raise ValueError("Invalid image extension")

        if image.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
            raise ValueError("Invalid image content type")

        image_content = image.file.read()
        image.file.seek(0)

        if not image_content:
            raise ValueError("Image file is empty")

        max_size_bytes = settings.max_image_size_mb * 1024 * 1024
        if len(image_content) > max_size_bytes:
            raise ValueError(f"Image file exceeds {settings.max_image_size_mb} MB")

        if extension in {".jpg", ".jpeg"}:
            is_valid_image = image_content.startswith(b"\xff\xd8\xff")
        else:
            is_valid_image = image_content.startswith((b"II*\x00", b"MM\x00*"))

        if not is_valid_image:
            raise ValueError("Image file appears to be corrupted or invalid")

        return image_content

    def process_image(
        self,
        db: Session,
        inference_request: InferenceRequest,
        image: UploadFile,
    ) -> InferenceResponse:
        mission = get_mission(db, inference_request.mission_id)
        if mission is None:
            raise ValueError("Mission not found")

        try:
            self.validate_image(image)
            prediction_result = model_service.predict(image)
            prediction = register_prediction_result(
                db=db,
                mission_id=inference_request.mission_id,
                model_name=prediction_result["model_name"],
                model_version=prediction_result["model_version"],
                inference_time=prediction_result["inference_time"],
                status="success",
                result=prediction_result["result"],
            )
        except Exception as exc:
            prediction = register_prediction_result(
                db=db,
                mission_id=inference_request.mission_id,
                model_name=model_service.model_name,
                model_version=model_service.model_version,
                inference_time=0,
                status="failed",
                error_message=str(exc),
            )
            return InferenceResponse(
                prediction_id=prediction.id,
                status=prediction.status,
                model_version=prediction.model_version,
                inference_time=prediction.inference_time,
                result=prediction.result,
            )

        return InferenceResponse(
            prediction_id=prediction.id,
            status=prediction.status,
            model_version=prediction.model_version,
            inference_time=prediction.inference_time,
            result=prediction.result,
        )


ai_processing_service = AIProcessingService()
