from typing import List

from returns.maybe import Maybe, Some, Nothing
from returns.result import Result, Success, Failure

from app.db.database import session_maker
from app.db.models import Target, Mission
from app.gql.mutations.mission_mutations import MissionResultInput


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


def insert_target(target: Target) -> Result[Target, str]:
    with session_maker() as session:
        try:
            session.add(target)
            session.commit()
            session.refresh(target)
            return Success(target)
        except Exception as e:
            session.rollback()
            return Failure(str(e))


def update_mission_result(mission_result_input: MissionResultInput) -> Result[Mission, str]:
    with session_maker() as session:
        try:
            mission_to_update = session.get(Mission, mission_result_input.mission_id)
            mission_to_update.aircraft_lost = mission_result_input.aircraft_lost
            mission_to_update.aircraft_returned = mission_result_input.aircraft_returned
            mission_to_update.aircraft_damaged = mission_result_input.aircraft_damaged
            mission_to_update.aircraft_failed = mission_result_input.aircraft_failed
            session.commit()
            session.refresh(mission_to_update)
            return Success(mission_to_update)
        except Exception as e:
            session.rollback()
            return Failure(str(e))