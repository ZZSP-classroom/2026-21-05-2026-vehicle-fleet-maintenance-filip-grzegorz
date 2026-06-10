from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "VehicleFleetMaintenance"
    APP_VERSION: str = "0.1.0"
    DATABASE_URL: str = "sqlite:///./fleet.db"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
