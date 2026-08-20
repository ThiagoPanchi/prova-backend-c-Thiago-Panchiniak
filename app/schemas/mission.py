from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MissionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    status: str = Field(..., min_length=1, max_length=100)
    drone_model: str = Field(..., min_length=1, max_length=255)
    image_count: int = Field(..., ge=0)
    area_hectares: float = Field(..., gt=0)


class MissionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    status: str | None = Field(default=None, min_length=1, max_length=100)
    drone_model: str | None = Field(default=None, min_length=1, max_length=255)
    image_count: int | None = Field(default=None, ge=0)
    area_hectares: float | None = Field(default=None, gt=0)


class MissionResponse(BaseModel):
    id: int
    name: str
    status: str
    created_at: datetime
    drone_model: str
    image_count: int
    area_hectares: float

    model_config = ConfigDict(from_attributes=True)
