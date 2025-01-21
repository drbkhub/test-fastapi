from database.engine import engine
from database.base import Base
from database.user import User

Base.metadata.create_all(engine)
