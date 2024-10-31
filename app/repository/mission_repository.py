from typing import List

from returns.maybe import Maybe, Nothing, Some
from returns.result import Result, Success, Failure
from sqlalchemy import and_

from app.db.database import session_maker
from app.db.models import Mission, Country, Target, City, TargetType


def find_mission_by_id(mission_id: int) -> Maybe[Mission]:
    with session_maker() as session:
        try:
            mission: Mission = session.get(Mission, mission_id)
            if not mission:
                return Nothing
            return Some(mission)
        except Exception:
            return Nothing


def find_missions_by_date_range(start_date, end_date) -> List[Mission]:
    with session_maker() as session:
        return (
            session.query(Mission)
                .filter(and_(Mission.mission_date >= start_date, Mission.mission_date <= end_date))
                .all()
            )


def find_missions_by_country_name(country_name: str) -> List[Mission]:
    with session_maker() as session:
        return (
            session.query(Mission)
            .join(Target, Mission.mission_id == Target.mission_id)
            .join(City, City.city_id == Target.city_id)
            .join(Country, Country.country_id == City.country_id)
            .filter(Country.country_name == country_name)
            .all()
        )


def find_missions_target_industry(target_industry: str) -> List[Mission]:
    with session_maker() as session:
        return (
            session.query(Mission)
            .join(Target, Target.mission_id == Mission.mission_id)
            .filter(Target.target_industry == target_industry)
            .all()
        )


def find_missions_by_target_type(target_type: str) -> List[Mission]:
    with session_maker() as session:
        return (
            session.query(Mission)
            .join(Target, Target.mission_id == Mission.mission_id)
            .join(TargetType, TargetType.target_type_id == Target.target_type_id)
            .filter(TargetType.target_type_name == target_type)
            .all()
        )


def insert_mission(mission: Mission) -> Result[Mission, str]:
    with session_maker() as session:
        try:
            session.add(mission)
            session.commit()
            session.refresh(mission)
            return Success(mission)
        except Exception as e:
            session.rollback()
            return Failure(str(e))


def delete_mission_by_id(mission_id: int) -> Result[bool, str]:
    with session_maker() as session:
        try:
            mission_to_delete = session.get(Mission, mission_id)
            session.delete(mission_to_delete)
            session.commit()
            return Success(True)
        except Exception as e:
            session.rollback()
            return Failure(str(e))