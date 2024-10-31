from typing import List

from returns.maybe import Maybe, Nothing, Some

from app.db.database import session_maker
from app.db.models import City


def find_cities_by_country_id(country_id: int) -> List[City]:
    with session_maker() as session:
        return session.query(City).filter_by(country_id=country_id).all()


def find_city_by_id(city_id) -> Maybe[City]:
    with session_maker() as session:
        try:
            city: City = session.get(City, city_id)
            if not city:
                return Nothing
            return Some(city)
        except Exception:
            return Nothing