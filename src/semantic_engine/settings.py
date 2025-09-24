from pydantic import BaseSettings
class Settings(BaseSettings):
    app_name: str = 'Semantic Engine'
settings = Settings()