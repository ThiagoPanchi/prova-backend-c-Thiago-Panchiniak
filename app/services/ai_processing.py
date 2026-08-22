import time
from typing import Any

from app.core.config import settings

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
