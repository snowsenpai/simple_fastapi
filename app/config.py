from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str
    pg_db_url: str

    class Config:
        env_file = ".env"

settings = Settings()