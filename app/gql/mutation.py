from graphene import ObjectType

from app.gql.mutations.mission_mutations import AddMission, AddTarget


class Mutation(ObjectType):
    add_mission = AddMission.Field()
    add_target_related_to_mission = AddTarget.Field()