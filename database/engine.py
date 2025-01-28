from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.exc import OperationalError

from settings import DATABASE_URL
from .models.base import Base


engine = create_async_engine(DATABASE_URL)

# try:
#     with engine.connect() as connection:
#         print("Успешное подключение к базе данных!")
# except OperationalError as e:
#     print("Ошибка подключения к базе данных:")
#     print(e)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
