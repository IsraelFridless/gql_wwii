from graphene import ObjectType, Field, Int, List, Date, String
from returns.maybe import Nothing
from sqlalchemy.exc import SQLAlchemyError

from app.gql.types import MissionType
from app.repository.mission_repository import find_mission_by_id, find_missions_by_date_range, \
    find_missions_by_country_name, find_missions_target_industry, find_missions_by_target_type


class Query(ObjectType):
    mission_by_id = Field(MissionType, mission_id=Int())
    missions_by_date_range = List(MissionType, start_date=Date(), end_date=Date())
    missions_by_country_name = List(MissionType, country_name=String())
    missions_by_target_industry = List(MissionType, target_industry=String())
    missions_by_target_type = List(MissionType, target_type=String())

    @staticmethod
    def resolve_mission_by_id(root, info, mission_id):
        maybe_mission = find_mission_by_id(mission_id)
        if maybe_mission is Nothing:
            raise SQLAlchemyError(f'mission with id: {mission_id} not found')
        return maybe_mission.value_or(None)

    @staticmethod
    def resolve_missions_by_date_range(root, info, start_date, end_date):
        return find_missions_by_date_range(start_date, end_date)

    @staticmethod
    def resolve_missions_by_country_name(root, info, country_name):
        return find_missions_by_country_name(country_name)

    @staticmethod
    def resolve_missions_by_target_industry(root, info, target_industry):
        return find_missions_target_industry(target_industry)

    @staticmethod
    def resolve_missions_by_target_type(root, info, target_type):
        return find_missions_by_target_type(target_type)