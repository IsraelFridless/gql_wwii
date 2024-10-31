from returns.maybe import Maybe, Some, Nothing

from app.db.database import session_maker
from app.db.models import TargetType


def find_target_type_by_id(target_type_id: int) -> Maybe[TargetType]:
    with session_maker() as session:
        try:
            target_type: TargetType = session.get(TargetType, target_type_id)
            if not target_type:
                return Nothing
            return Some(target_type)
        except Exception:
            return Nothing