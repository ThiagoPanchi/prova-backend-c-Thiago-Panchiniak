import time
from typing import Any

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.repositories.mission import get_mission
from app.repositories.prediction_history import create_prediction_history
from app.schemas import InferenceRequest, InferenceResponse

MODEL_NAME = "aerial_mapping_yolo"
MODEL_VERSION = "1.0.0"


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
    def process_image(
        self,
        db: Session,
        inference_request: InferenceRequest,
        image: UploadFile,
    ) -> InferenceResponse:
        mission = get_mission(db, inference_request.mission_id)
        if mission is None:
            raise ValueError("Mission not found")

        if image.content_type is None or not image.content_type.startswith("image/"):
            raise ValueError("Uploaded file must be an image")

        try:
            prediction_result = model_service.predict(image)
            prediction = create_prediction_history(
                db=db,
                mission_id=inference_request.mission_id,
                model_name=prediction_result["model_name"],
                model_version=prediction_result["model_version"],
                inference_time=prediction_result["inference_time"],
                status="completed",
                result=prediction_result["result"],
            )
        except Exception as exc:
            prediction = create_prediction_history(
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
