from sqlalchemy.orm import declarative_base, DeclarativeMeta

Base: DeclarativeMeta = declarative_base()

from .country import Country
from .city import City
from .target import Target
from .mission import Mission
from .target_type import TargetType