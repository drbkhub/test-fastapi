from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("Успешное подключение к базе данных!")
except OperationalError as e:
    print("Ошибка подключения к базе данных:")
    print(e)
