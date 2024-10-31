from typing import List

from app.db.database import session_maker
from app.db.models import City


def find_cities_by_country_id(country_id: int) -> List[City]:
    with session_maker() as session:
        return session.query(City).filter_by(country_id=country_id).all()