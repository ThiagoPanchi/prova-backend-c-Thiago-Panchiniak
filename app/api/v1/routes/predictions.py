from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.prediction_history import (
    get_prediction,
    get_predictions,
    get_predictions_by_mission,
)
from app.schemas import PredictionResponse

router = APIRouter(tags=["predictions"])


@router.get("/predictions", response_model=list[PredictionResponse])
def get_predictions_route(db: Session = Depends(get_db)):
    return get_predictions(db)


@router.get("/predictions/{id}", response_model=PredictionResponse)
def get_prediction_route(id: int, db: Session = Depends(get_db)):
    prediction = get_prediction(db, id)
    if prediction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found",
        )
    return prediction


@router.get("/missions/{mission_id}/predictions", response_model=list[PredictionResponse])
def get_predictions_by_mission_route(
    mission_id: int,
    db: Session = Depends(get_db),
):
    return get_predictions_by_mission(db, mission_id)
