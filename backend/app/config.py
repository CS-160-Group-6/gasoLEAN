from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database configuration
    DB_URL: str = Field('sqlite:///./data.db', env='DB_URL')

settings = Settings()