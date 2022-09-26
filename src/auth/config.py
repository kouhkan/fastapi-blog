from datetime import timedelta

from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    access_expires: int = timedelta(days=14)
    refresh_expires: int = timedelta(days=30)


settings = Settings()


@AuthJWT.load_config
def get_config():
    return settings
