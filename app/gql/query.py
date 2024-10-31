from graphene import ObjectType, Field, Int, List

from app.db.database import session_maker
from app.db.models import Mission
from app.gql.types.mission_types import MissionType
from app.repository.mission_repository import find_mission_by_id


class Query(ObjectType):
    mission_by_id = Field(MissionType, mission_id=Int())
    missions_by_date_range = List(MissionType)

    @staticmethod
    def resolve_mission_by_id(root, info, mission_id):
        maybe_mission = find_mission_by_id(mission_id)
        return maybe_mission.value_or(f'mission with id: {mission_id} not found')

    @staticmethod
    def resolve_missions_by_date_range(root, info):
        return find_missions_by_date_range()