import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional
from app.models.schemas import SpotifyToken
from app.config import settings


class TokenService:
    def __init__(self):
        self.session_tokens: Dict[str, dict] = {}
        self.spotify_tokens: Dict[str, SpotifyToken] = {}
        self.session_expires_in = 7 * 24 * 60 * 60
    
    def create_session_token(self, spotify_user_id: str, spotify_token: SpotifyToken) -> str:
        session_token = secrets.token_urlsafe(32)
        
        self.session_tokens[session_token] = {
            "spotify_user_id": spotify_user_id,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(seconds=self.session_expires_in)
        }
        
        self.spotify_tokens[spotify_user_id] = spotify_token
        
        print(f"[TokenService] Token created for user {spotify_user_id}: {session_token[:20]}...")
        print(f"[TokenService] Spotify access_token expires in: {spotify_token.expires_in}s")
        print(f"[TokenService] Total sessions: {len(self.session_tokens)}")
        print(f"[TokenService] Total spotify tokens: {len(self.spotify_tokens)}")
        
        return session_token
    
    def validate_session_token(self, session_token: str) -> Optional[dict]:
        session_data = self.session_tokens.get(session_token)
        
        if not session_data:
            print(f"[TokenService] Token not found: {session_token[:20]}...")
            print(f"[TokenService] Available tokens: {list(self.session_tokens.keys())[:3]}")
            return None
        
        if datetime.utcnow() > session_data["expires_at"]:
            print(f"[TokenService] Token expired for: {session_data['spotify_user_id']}")
            del self.session_tokens[session_token]
            return None
        
        print(f"[TokenService] Token validated for: {session_data['spotify_user_id']}")
        return session_data
    
    def get_spotify_token(self, spotify_user_id: str) -> Optional[str]:
        token = self.spotify_tokens.get(spotify_user_id)
        
        if not token:
            print(f"[TokenService] Spotify token not found for user: {spotify_user_id}")
            return None
        
        if datetime.utcnow() > token.expires_at:
            print(f"[TokenService] Spotify token expired for: {spotify_user_id}")
            return None
        
        return token.access_token
    
    def get_refresh_token(self, spotify_user_id: str) -> Optional[str]:
        token = self.spotify_tokens.get(spotify_user_id)
        
        if not token:
            return None
        
        return token.refresh_token
    
    def update_spotify_token(self, spotify_user_id: str, token: SpotifyToken):
        self.spotify_tokens[spotify_user_id] = token
    
    def invalidate_session(self, session_token: str):
        if session_token in self.session_tokens:
            del self.session_tokens[session_token]


# Singleton global
token_service = TokenService()
