from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    # --------------------
    # App
    # --------------------
    APP_NAME: str = "MallNet"
    ENV: str = "development"

    # --------------------
    # Database
    # --------------------
    DATABASE_URL: str = "sqlite:///./mallnet.db"

    # --------------------
    # MikroTik
    # --------------------
    MIKROTIK_HOST: str
    MIKROTIK_USER: str
    MIKROTIK_PASS: str
    MIKROTIK_PORT: int = 8728

    # --------------------
    # Payments (PayNow)
    # --------------------
    PAYNOW_INTEGRATION_ID: Optional[str] = None
    PAYNOW_INTEGRATION_KEY: Optional[str] = None
    PAYNOW_RETURN_URL: Optional[str] = None
    PAYNOW_RESULT_URL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="forbid",   # keep this strict (GOOD)
    )


settings = Settings()
