from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DB_HOST: str
    # DB_PORT: int
    # DB_USER: str
    # DB_PASS: str
    # DB_NAME: str

    ALGORITHM: str

    class Config:
        env_file = ".env"


settings = Settings()


BASE_DIR = Path(__file__).parent.parent


class AuthSettings(BaseSettings):
    private_key_pass: Path = BASE_DIR / "secret_key.pem"


auth_settings = AuthSettings()
