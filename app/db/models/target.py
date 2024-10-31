from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models import Base


class Target(Base):
    __tablename__ = "targets"
    target_id = Column(Integer, primary_key=True, autoincrement=True)
    mission_id = Column(Integer, ForeignKey('missions.id'))
    city_id = Column(Integer, ForeignKey('cities.id'))
    target_type_id = Column(Integer, ForeignKey('targettypes.id'))
    target_industry = Column(String, nullable=False)
    target_priority = Column(Integer, nullable=False)

    mission = relationship(
        'Mission',
        back_populates='target'
    )

    target_type = relationship(
        'TargetType',
        back_populates='target',
        cascade='all, delete-orphan'
    )
