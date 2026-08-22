from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.repositories.prediction_history import (
    delete_prediction,
    get_prediction,
    get_predictions,
    get_predictions_by_mission,
    update_prediction,
)
from app.schemas import PredictionResponse, PredictionUpdate

router = APIRouter(
    tags=["predictions"],
    dependencies=[Depends(get_current_user)],
)


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


@router.put("/predictions/{id}", response_model=PredictionResponse)
def update_prediction_route(
    id: int,
    prediction_data: PredictionUpdate,
    db: Session = Depends(get_db),
):
    prediction = update_prediction(db, id, prediction_data)
    if prediction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found",
        )
    return prediction


@router.delete("/predictions/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prediction_route(id: int, db: Session = Depends(get_db)):
    deleted = delete_prediction(db, id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found",
        )
