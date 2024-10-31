from typing import List

from returns.maybe import Maybe, Some, Nothing

from app.db.database import session_maker
from app.db.models import Target


def find_target_by_mission_id(mission_id) -> Maybe[Target]:
    with session_maker() as session:
        try:
            target: Target = session.query(Target).filter_by(mission_id=mission_id).first()
            if not target:
                return Nothing
            return Some(target)
        except Exception:
            return Nothing


def find_targets_by_target_type_id(target_type_id: int) -> List[Target]:
    with session_maker() as session:
        return session.query(Target).filter_by(target_type_id=target_type_id).all()


def find_targets_by_city_id(city_id) -> List[Target]:
    with session_maker() as session:
        return session.query(Target).filter_by(city_id=city_id).all()