from authx import AuthXConfig, AuthX
from punq import Container
from config.settings import Settings


def init_authx(settings: Settings):
    config = AuthXConfig()
    config.JWT_SECRET_KEY = settings.jwt_secret_key
    config.JWT_TOKEN_LOCATION = ["cookies"]


    return AuthX(config=config)