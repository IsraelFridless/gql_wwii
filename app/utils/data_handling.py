from datetime import datetime
from functools import partial

from sqlalchemy import func
from toolz import pipe

from sqlalchemy.orm import class_mapper
from app.db.database import session_maker
from app.db.models import Mission


def parse_date_string(date_string: str):
    try:
        parsed_date = datetime.strptime(date_string,"%Y/%m/%d").date()
        return parsed_date
    except ValueError as e:
        raise ValueError(f"Invalid date string '{date_string}': {e}")

def generate_mission_id() -> int:
    with session_maker() as session:
        return session.query(func.max(Mission.mission_id)).scalar() + 1
