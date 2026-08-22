from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class InferenceRequest(BaseModel):
    mission_id: int = Field(..., gt=0)
    confidence_threshold: float = Field(..., ge=0, le=1)


class InferenceResponse(BaseModel):
    prediction_id: int
    status: str
    model_version: str
    inference_time: float
    result: dict[str, Any] | None = None


class PredictionUpdate(BaseModel):
    model_name: str | None = Field(default=None, min_length=1)
    model_version: str | None = Field(default=None, min_length=1)
    inference_time: float | None = Field(default=None, ge=0)
    status: str | None = Field(default=None, min_length=1)
    result: dict[str, Any] | None = None
    error_message: str | None = None


class PredictionResponse(BaseModel):
    id: int
    mission_id: int
    created_at: datetime
    model_name: str
    model_version: str
    inference_time: float
    status: str
    result: dict[str, Any] | None = None
    error_message: str | None = None

    model_config = ConfigDict(from_attributes=True)
