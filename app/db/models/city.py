from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.models import Base


class City(Base):
    __tablename__ = "cities"
    city_id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    country_id = Column(Integer, ForeignKey('countries.country_id'))

    country = relationship(
        'Country',
        back_populates='cities'
    )

    targets = relationship(
        'Target',
        back_populates='city'
    )