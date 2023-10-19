from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    database_host_name: str
    database_user_name: str
    database_port: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        # env_file = ".env"
        env_file = f"{Path(__file__).resolve().parent}\.env"
        # print("env_file", env_file)


settings = Settings()
