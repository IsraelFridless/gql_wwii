from graphene import InputObjectType, Int, String, Mutation, Field, Boolean, Date, Float
from returns.result import Success

from app.db.models import Mission
from app.gql.types.mission_types import MissionType
from app.repository.mission_repository import insert_mission
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
        print(mission_to_insert)
        result = insert_mission(mission_to_insert)

        message = 'successfully inserted' if isinstance(result, Success) else result.failure()
        mission = result.value_or(None)

        return AddMission(
            mission=mission,
            message=message
        )