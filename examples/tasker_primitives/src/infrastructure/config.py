from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    environment: str = Field(
        "production", description="App environment (production, test)"
    )
    database_url: str = Field(
        ..., env="DATABASE_URL", description="Database connection URL"
    )

    class Config:
        env_file = ".env"  # Automatically load environment variables from .env file
        env_file_encoding = "utf-8"


# Instantiate the settings singleton
settings = Settings()
