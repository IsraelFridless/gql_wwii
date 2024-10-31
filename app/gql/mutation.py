from graphene import ObjectType

from app.gql.mutations.mission_mutations import AddMission


class Mutation(ObjectType):
    add_mission = AddMission.Field()