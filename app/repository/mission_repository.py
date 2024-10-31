from returns.maybe import Maybe, Nothing, Some

from app.db.database import session_maker
from app.db.models import Mission


def find_mission_by_id(mission_id: int) -> Maybe[Mission]:
    with session_maker() as session:
        try:
            mission: Mission = session.get(Mission, mission_id)
            print(mission)
            if not mission:
                return Nothing
            return Some(mission)
        except Exception:
            return Nothing