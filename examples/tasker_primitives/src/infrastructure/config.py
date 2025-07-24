from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application configuration with environment variable binding."""

    environment: str = Field(
        "application",
        description="Application environment (test | application)",
        alias="ENVIRONMENT",
    )

    debug: bool = Field(
        False,
        description="Enable debug mode",
        alias="DEBUG",
    )

    log_level: str = Field(
        "INFO",
        description="Logging level",
        alias="LOG_LEVEL",
    )

    database_url: str = Field(
        ...,
        description="Database connection URL",
        alias="DATABASE_URL",
    )

    secret_key: str = Field(
        ...,
        description="Secret key for JWT token generation",
        alias="SECRET_KEY",
    )

    access_token_expires_in: int = Field(
        ...,
        description="Access token expiration time in seconds",
        alias="ACCESS_TOKEN_EXPIRES_IN",
    )

    refresh_token_expires_in: int = Field(
        ...,
        description="Refresh token expiration time in seconds",
        alias="REFRESH_TOKEN_EXPIRES_IN",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        arbitrary_types_allowed=True,
        from_attributes=True,
    )


app_settings = AppSettings()  # Singleton instance for easy access


def get_app_settings() -> AppSettings:
    return app_settings
