from pydantic_settings import BaseSettings


class MikroTikSettings(BaseSettings):
    MIKROTIK_HOST: str
    MIKROTIK_USER: str
    MIKROTIK_PASS: str
    MIKROTIK_PORT: int = 8728

    class Config:
        env_file = ".env"
        extra = "ignore"


mikrotik_settings = MikroTikSettings()
