from graphene import ObjectType, Int, String, Date, List, Float, Field
from returns.maybe import Nothing
from sqlalchemy.exc import SQLAlchemyError

from app.repository.city_repository import find_cities_by_country_id, find_city_by_id
from app.repository.country_repository import find_country_by_id
from app.repository.mission_repository import find_mission_by_id
from app.repository.target_repository import find_target_by_mission_id, find_targets_by_target_type_id, \
    find_targets_by_city_id
from app.repository.target_type_repository import find_target_type_by_id


class CityType(ObjectType):
    city_id = Int()
    city_name = String()
    latitude = Float()
    longitude = Float()
    country_id = Int()

    country = Field(lambda: CountryType)
    targets = Field(lambda: TargetType)

    @staticmethod
    def resolve_targets(root, info):
        return find_targets_by_city_id(root.city_id)

    @staticmethod
    def resolve_country(root, info):
        maybe_country = find_country_by_id(root.country_id)
        if maybe_country is Nothing:
            raise SQLAlchemyError(f'country with id: {root.country_id} not found')
        return maybe_country.value_or(None)


class MissionType(ObjectType):
    mission_id = Int()
    mission_date = Date()
    airborne_aircraft = Float()
    attacking_aircraft = Float()
    bombing_aircraft = Float()
    aircraft_returned = Float()
    aircraft_failed = Float()
    aircraft_damaged = Float()
    aircraft_lost = Float()

    target = Field(lambda: TargetType)

    @staticmethod
    def resolve_target(root, info):
        maybe_target = find_target_by_mission_id(root.mission_id)
        if maybe_target is Nothing:
            raise SQLAlchemyError(f'target with mission_id: {root.mission_id} not found')
        return maybe_target.value_or(None)


class TargetType(ObjectType):
    target_id = Int()
    mission_id = Int()
    city_id = Int()
    target_type_id = Int()
    target_industry = String
    target_priority = Int()

    mission = Field(lambda: MissionType)
    target_type = Field(lambda: TargetTypeType)
    city = Field(lambda: CityType)

    @staticmethod
    def resolve_city(root, info):
        maybe_city = find_city_by_id(root.city_id)
        if maybe_city is Nothing:
            raise SQLAlchemyError(f'city with id: {root.city_id} not found')
        return maybe_city.value_or(None)

    @staticmethod
    def resolve_mission(root, info):
        maybe_mission = find_mission_by_id(root.mission_id)
        if maybe_mission is Nothing:
            raise SQLAlchemyError(f'mission with id: {root.mission_id} not found')
        return maybe_mission.value_or(None)

    @staticmethod
    def resolve_target_type(root, info):
        maybe_target_type = find_target_type_by_id(root.target_type_id)
        if maybe_target_type is Nothing:
            raise SQLAlchemyError(f'target_type with id: {root.target_type_id} not found')
        return maybe_target_type.value_or(None)


class TargetTypeType(ObjectType):
    target_type_id = Int()
    target_type_name = String()

    targets = List(lambda: TargetType)

    @staticmethod
    def resolve_targets(root, info):
        return find_targets_by_target_type_id(root.target_type_id)


class CountryType(ObjectType):
    country_id = Int()
    country_name = String()

    cities = List(lambda: CityType)

    @staticmethod
    def resolve_cities(root, info):
        return find_cities_by_country_id(root.country_id)