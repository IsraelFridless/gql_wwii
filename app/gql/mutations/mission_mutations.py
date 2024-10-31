from graphene import InputObjectType, Int, String, Mutation, Field, Boolean, Date, Float
from returns.result import Success

from app.db.models import Mission, Target
from app.gql.types import *
from app.repository.mission_repository import insert_mission, delete_mission_by_id
from app.repository.target_repository import insert_target, update_mission_result
from app.utils.data_handling import parse_date_string, generate_mission_id


def has_none_fields(instance):
    return any(value is None for value in vars(instance).values())

class MissionInput(InputObjectType):
    mission_date = String()
    airborne_aircraft = Float()
    attacking_aircraft = Float()
    bombing_aircraft = Float()
    aircraft_returned = Float()
    aircraft_failed = Float()
    aircraft_damaged = Float()
    aircraft_lost = Float()

class TargetInput(InputObjectType):
    mission_id = Int(required=True)
    city_id = Int()
    target_type_id = Int()
    target_industry = String()
    target_priority = Int()

class MissionResultInput(InputObjectType):
    mission_id = Int(required=True)
    aircraft_returned = Float()
    aircraft_failed = Float()
    aircraft_damaged = Float()
    aircraft_lost = Float()


class AddMission(Mutation):
    class Arguments:
        mission_input = MissionInput(required=True)

    mission = Field(MissionType)
    message = String()

    @staticmethod
    def mutate(root, info, mission_input):
        mission_to_insert = Mission(
            mission_id=generate_mission_id(),
            mission_date=parse_date_string(mission_input.mission_date),
            airborne_aircraft=mission_input.airborne_aircraft,
            attacking_aircraft=mission_input.attacking_aircraft,
            bombing_aircraft=mission_input.bombing_aircraft,
            aircraft_returned=mission_input.aircraft_returned,
            aircraft_failed=mission_input.aircraft_failed,
            aircraft_damaged=mission_input.aircraft_damaged,
            aircraft_lost=mission_input.aircraft_lost
        )
        result = insert_mission(mission_to_insert)

        message = 'successfully inserted' if isinstance(result, Success) else result.failure()
        mission = result.value_or(None)

        return AddMission(
            mission=mission,
            message=message
        )

class AddTarget(Mutation):
    class Arguments:
        target_input = TargetInput(required=True)

    target = Field(TargetType)
    message = String()

    @staticmethod
    def mutate(root, info, target_input):
        target_to_insert = Target(
            mission_id=target_input.mission_id,
            city_id=target_input.city_id,
            target_type_id=target_input.target_type_id,
            target_industry=target_input.target_industry,
            target_priority=target_input.target_priority
        )
        result = insert_target(target_to_insert)

        message = 'successfully inserted' if isinstance(result, Success) else result.failure()
        target = result.value_or(None)

        return AddTarget(
            target=target,
            message=message
        )


class UpdateMissionResult(Mutation):
    class Arguments:
        mission_result_input = MissionResultInput(required=True)

    updated_mission = Field(MissionType)
    message = String()

    @staticmethod
    def mutate(root, info, mission_result_input):
        result = update_mission_result(mission_result_input)
        message = 'successfully updated' if isinstance(result, Success) else result.failure()
        updated_mission = result.value_or(None)

        return UpdateMissionResult(
            updated_mission=updated_mission,
            message=message
        )

class DeleteMission(Mutation):
    class Arguments:
        mission_id = Int()

    success = Boolean()
    message = String()

    @staticmethod
    def mutate(root, info, mission_id):
        result = delete_mission_by_id(mission_id)
        message = 'successfully deleted' if isinstance(result, Success) else result.failure()

        return DeleteMission(
            success=result.value_or(False),
            message=message
        )
