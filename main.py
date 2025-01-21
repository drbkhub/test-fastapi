from database.engine import engine
from database.base import Base

Base.metadata.create_all(engine)
