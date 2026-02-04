from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class PaynowSettings(BaseSettings):
    PAYNOW_INTEGRATION_ID: Optional[str] = None
    PAYNOW_INTEGRATION_KEY: Optional[str] = None
    PAYNOW_RETURN_URL: Optional[str] = None
    PAYNOW_RESULT_URL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",   # 🔥 THIS IS THE KEY
    )


paynow_settings = PaynowSettings()
