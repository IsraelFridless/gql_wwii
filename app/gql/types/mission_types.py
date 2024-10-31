from graphene import ObjectType, Int, String, Date, List


class CityType(ObjectType):
    pass

class MissionType(ObjectType):
    pass

class TargetType(ObjectType):
    pass

class TargetTypeType(ObjectType):
    pass


class CountryType(ObjectType):
    country_id = Int()
    country_name = String()

    cities = List(lambda: CityType)