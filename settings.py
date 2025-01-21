from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_name: str = Field(default="database", env="DB_NAME")
    db_user: str = Field(default="postgres", env="DB_USER")
    db_password: str = Field(default="password", env="DB_PASSWORD")

    class Config:
        env_file = ".env"


db_settings = DatabaseSettings()

DATABASE_URL = (
    f"postgresql+psycopg2://{db_settings.db_user}:{db_settings.db_password}@"
    f"{db_settings.db_host}:{db_settings.db_port}/{db_settings.db_name}"
)
