from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Mission
from app.schemas import MissionCreate, MissionUpdate


def create_mission(db: Session, mission_data: MissionCreate) -> Mission:
    mission = Mission(**mission_data.model_dump())
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission


def get_mission(db: Session, mission_id: int) -> Mission | None:
    return db.get(Mission, mission_id)


def get_missions(db: Session) -> list[Mission]:
    return list(db.scalars(select(Mission)).all())


def update_mission(db: Session, mission_id: int, mission_data: MissionUpdate) -> Mission | None:
    mission = get_mission(db, mission_id)
    if mission is None:
        return None

    for field, value in mission_data.model_dump(exclude_unset=True).items():
        setattr(mission, field, value)

    db.commit()
    db.refresh(mission)
    return mission


def delete_mission(db: Session, mission_id: int) -> bool:
    mission = get_mission(db, mission_id)
    if mission is None:
        return False

    db.delete(mission)
    db.commit()
    return True
