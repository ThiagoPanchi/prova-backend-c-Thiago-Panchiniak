from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import InferenceRequest, InferenceResponse
from app.services.ai_processing import ai_processing_service

router = APIRouter(prefix="/ai-processing", tags=["ai-processing"])


@router.post("/process", response_model=InferenceResponse)
def process_image(
    mission_id: int = Form(...),
    confidence_threshold: float = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        inference_request = InferenceRequest(
            mission_id=mission_id,
            confidence_threshold=confidence_threshold,
        )
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.errors(),
        ) from exc

    try:
        return ai_processing_service.process_image(db, inference_request, image)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
