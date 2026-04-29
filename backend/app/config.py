from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    REDIRECT_URI: str
    FRONTEND_URL: str
    SECRET_KEY: str
    SPOTIFY_AUTH_URL: str = "https://accounts.spotify.com/authorize"
    SPOTIFY_TOKEN_URL: str = "https://accounts.spotify.com/api/token"
    SPOTIFY_API_BASE_URL: str = "https://api.spotify.com/v1"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_ENABLED: bool = True

    SPOTIFY_SCOPES: List[str] = [
        "user-read-private",
        "user-read-email",
        "user-top-read",
        "playlist-modify-public",
        "playlist-modify-private"
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
