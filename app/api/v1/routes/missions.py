from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.mission import (
    create_mission,
    delete_mission,
    get_mission,
    get_missions,
    update_mission,
)
from app.schemas import MissionCreate, MissionResponse, MissionUpdate

router = APIRouter(prefix="/missions", tags=["missions"])


@router.post("/", response_model=MissionResponse, status_code=status.HTTP_201_CREATED)
def create_mission_route(mission_data: MissionCreate, db: Session = Depends(get_db)):
    return create_mission(db, mission_data)


@router.get("/", response_model=list[MissionResponse])
def get_missions_route(db: Session = Depends(get_db)):
    return get_missions(db)


@router.get("/{mission_id}", response_model=MissionResponse)
def get_mission_route(mission_id: int, db: Session = Depends(get_db)):
    mission = get_mission(db, mission_id)
    if mission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")
    return mission


@router.put("/{mission_id}", response_model=MissionResponse)
def update_mission_route(
    mission_id: int,
    mission_data: MissionUpdate,
    db: Session = Depends(get_db),
):
    mission = update_mission(db, mission_id, mission_data)
    if mission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")
    return mission


@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission_route(mission_id: int, db: Session = Depends(get_db)):
    deleted = delete_mission(db, mission_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")
