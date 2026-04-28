from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SpotifyToken(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"
    expires_at: datetime


class User(BaseModel):
    spotify_user_id: str
    email: str
    display_name: str
    images: List[dict] = []
    country: Optional[str] = None
    product: Optional[str] = None


class Track(BaseModel):
    id: str
    name: str
    artists: List[dict]
    album: dict
    duration_ms: int
    preview_url: Optional[str] = None
    external_urls: dict
    audio_features: Optional[dict] = None


class Artist(BaseModel):
    id: str
    name: str
    genres: List[str] = []
    images: List[dict] = []
    external_urls: dict


class RecommendationRequest(BaseModel):
    limit: int = Field(default=20, ge=1, le=50)
    mood: Optional[str] = Field(default=None, description="happy, chill, workout, sad, energetic")


class RecommendationResponse(BaseModel):
    tracks: List[Track]
    user_vector: Optional[List[float]] = None
    explanation: Optional[str] = None


class PlaylistCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    track_uris: List[str]


class PlaylistCreateResponse(BaseModel):
    playlist_id: str
    playlist_url: str
    tracks_added: int


class UserProfileResponse(BaseModel):
    user: User
    top_tracks: List[Track]
    top_artists: List[Artist]


class AuthCallbackResponse(BaseModel):
    session_token: str
    redirect_url: str
