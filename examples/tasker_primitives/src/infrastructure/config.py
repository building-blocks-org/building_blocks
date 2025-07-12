from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application configuration with environment variable binding."""

    environment: str = Field(
        "application", description="Application environment (test | application)"
    )

    debug: bool = Field(False, description="Enable debug mode")

    log_level: str = Field("INFO", description="Logging level")

    database_url: str = Field(..., description="Database connection URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        arbitrary_types_allowed=True,
        from_attributes=True,
    )


app_settings = AppSettings()  # Singleton instance for easy access


# Factory functions for instantiation
def get_app_settings() -> AppSettings:
    return app_settings
