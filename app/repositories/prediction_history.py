from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import PredictionHistory
from app.schemas import PredictionUpdate


def register_prediction_result(
    db: Session,
    mission_id: int,
    model_name: str,
    model_version: str,
    inference_time: float,
    status: str,
    result: dict[str, Any] | None = None,
    error_message: str | None = None,
) -> PredictionHistory:
    prediction = PredictionHistory(
        mission_id=mission_id,
        model_name=model_name,
        model_version=model_version,
        inference_time=inference_time,
        status=status,
        result=result,
        error_message=error_message,
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


def get_predictions(db: Session) -> list[PredictionHistory]:
    return list(db.scalars(select(PredictionHistory)).all())


def get_prediction(db: Session, prediction_id: int) -> PredictionHistory | None:
    return db.get(PredictionHistory, prediction_id)


def get_predictions_by_mission(
    db: Session,
    mission_id: int,
) -> list[PredictionHistory]:
    return list(
        db.scalars(
            select(PredictionHistory).where(PredictionHistory.mission_id == mission_id)
        ).all()
    )


def update_prediction(
    db: Session,
    prediction_id: int,
    prediction_data: PredictionUpdate,
) -> PredictionHistory | None:
    prediction = get_prediction(db, prediction_id)
    if prediction is None:
        return None

    for field, value in prediction_data.model_dump(exclude_unset=True).items():
        setattr(prediction, field, value)

    db.commit()
    db.refresh(prediction)
    return prediction


def delete_prediction(db: Session, prediction_id: int) -> bool:
    prediction = get_prediction(db, prediction_id)
    if prediction is None:
        return False

    db.delete(prediction)
    db.commit()
    return True
