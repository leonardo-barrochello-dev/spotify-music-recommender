import httpx
from app.config import settings
from app.models.schemas import SpotifyToken, User
from datetime import datetime, timedelta
from typing import Optional, Dict
from urllib.parse import urlencode


class AuthService:
    def __init__(self):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.redirect_uri = settings.REDIRECT_URI
        self.auth_url = settings.SPOTIFY_AUTH_URL
        self.token_url = settings.SPOTIFY_TOKEN_URL
        self.scopes = " ".join(settings.SPOTIFY_SCOPES)
    
    def get_authorization_url(self, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": self.scopes,
            "state": state,
            "show_dialog": "true"
        }
        return f"{self.auth_url}?{urlencode(params)}"
    
    async def exchange_code_for_token(self, code: str) -> SpotifyToken:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": self.redirect_uri,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            response.raise_for_status()
            data = response.json()
            
            expires_at = datetime.utcnow() + timedelta(seconds=data["expires_in"])
            
            return SpotifyToken(
                access_token=data["access_token"],
                refresh_token=data["refresh_token"],
                expires_in=data["expires_in"],
                token_type=data["token_type"],
                expires_at=expires_at
            )
    
    async def refresh_access_token(self, refresh_token: str) -> SpotifyToken:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            response.raise_for_status()
            data = response.json()
            
            expires_at = datetime.utcnow() + timedelta(seconds=data["expires_in"])
            
            return SpotifyToken(
                access_token=data["access_token"],
                refresh_token=data.get("refresh_token", refresh_token),
                expires_in=data["expires_in"],
                token_type=data["token_type"],
                expires_at=expires_at
            )
