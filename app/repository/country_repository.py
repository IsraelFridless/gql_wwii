from returns.maybe import Maybe, Nothing, Some

from app.db.database import session_maker
from app.db.models import Country


def find_country_by_id(country_id: int) -> Maybe[Country]:
    with session_maker() as session:
        try:
            country: Country = session.get(Country, country_id)
            if not country:
                return Nothing
            return Some(country)
        except Exception:
            return Nothing