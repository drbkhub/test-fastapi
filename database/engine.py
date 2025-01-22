from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("Успешное подключение к базе данных!")
except OperationalError as e:
    print("Ошибка подключения к базе данных:")
    print(e)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
