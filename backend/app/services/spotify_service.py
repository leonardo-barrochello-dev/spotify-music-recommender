import httpx
import logging
from fastapi import HTTPException
from app.config import settings
from app.models.schemas import User, Track, Artist
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class SpotifyService:
    def __init__(self):
        self.api_base_url = settings.SPOTIFY_API_BASE_URL
    
    def _get_headers(self, access_token: str) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    async def get_current_user(self, access_token: str) -> User:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_base_url}/me",
                headers=self._get_headers(access_token)
            )
            response.raise_for_status()
            data = response.json()
            
            return User(
                spotify_user_id=data["id"],
                email=data["email"],
                display_name=data["display_name"] or data["id"],
                images=data.get("images", []),
                country=data.get("country"),
                product=data.get("product")
            )
    
    async def get_top_tracks(
        self,
        access_token: str,
        limit: int = 20,
        time_range: str = "medium_term"
    ) -> List[Track]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_base_url}/me/top/tracks",
                headers=self._get_headers(access_token),
                params={"limit": limit, "time_range": time_range}
            )
            response.raise_for_status()
            data = response.json()
            
            tracks = []
            for item in data["items"]:
                track = Track(
                    id=item["id"],
                    name=item["name"],
                    artists=[{"id": a["id"], "name": a["name"]} for a in item["artists"]],
                    album={
                        "id": item["album"]["id"],
                        "name": item["album"]["name"],
                        "images": item["album"]["images"]
                    },
                    duration_ms=item["duration_ms"],
                    preview_url=item.get("preview_url"),
                    external_urls=item["external_urls"]
                )
                tracks.append(track)
            
            return tracks
    
    async def get_top_artists(
        self,
        access_token: str,
        limit: int = 20,
        time_range: str = "medium_term"
    ) -> List[Artist]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_base_url}/me/top/artists",
                headers=self._get_headers(access_token),
                params={"limit": limit, "time_range": time_range}
            )
            response.raise_for_status()
            data = response.json()
            
            artists = []
            for item in data["items"]:
                artist = Artist(
                    id=item["id"],
                    name=item["name"],
                    genres=item.get("genres", []),
                    images=item.get("images", []),
                    external_urls=item["external_urls"]
                )
                artists.append(artist)
            
            return artists
    
    async def get_audio_features(
        self,
        access_token: str,
        track_ids: List[str]
    ) -> Dict[str, dict]:
        if not track_ids:
            return {}
        
        features = {}
        for i in range(0, len(track_ids), 100):
            batch_ids = track_ids[i:i+100]
            ids_param = ",".join(batch_ids)
            logger.info(f"Requesting audio-features for {len(batch_ids)} tracks...")
            logger.info(f"Full URL: {self.api_base_url}/audio-features?ids={','.join(batch_ids)}")
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/audio-features",
                    headers=self._get_headers(access_token),
                    params={"ids": ",".join(batch_ids)}
                )
                logger.info(f"Response status: {response.status_code}")
                
                if response.status_code == 403:
                    test_response = await client.get(
                        f"{self.api_base_url}/me",
                        headers=self._get_headers(access_token)
                    )
                    logger.info(f"Test /me status: {test_response.status_code}")
                    
                    if test_response.status_code == 403:
                        logger.error(f"403 on ALL endpoints - Token is REVOKED or invalid. User needs to login again.")
                        error_data = response.json()
                        logger.error(f"Full error response: {error_data}")
                        return {}
                    
                    logger.error(f"403 Forbidden on audio-features only - other endpoints work")
                    return {}
                
                if response.status_code >= 400:
                    logger.error(f"Response body: {response.text}")
                response.raise_for_status()
                data = response.json()
                
                for item in data["audio_features"]:
                    if item:
                        features[item["id"]] = item
        
        return features
    
    async def get_related_artists(
        self,
        access_token: str,
        artist_id: str
    ) -> List[Artist]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_base_url}/artists/{artist_id}/related-artists",
                headers=self._get_headers(access_token)
            )
            response.raise_for_status()
            data = response.json()
            
            artists = []
            for item in data["artists"]:
                artist = Artist(
                    id=item["id"],
                    name=item["name"],
                    genres=item.get("genres", []),
                    images=item.get("images", []),
                    external_urls=item["external_urls"]
                )
                artists.append(artist)
            
            return artists
    
    async def get_artist_top_tracks(
        self,
        access_token: str,
        artist_id: str,
        market: str = "US"
    ) -> List[Track]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_base_url}/artists/{artist_id}/top-tracks",
                headers=self._get_headers(access_token),
                params={"market": market}
            )
            response.raise_for_status()
            data = response.json()
            
            tracks = []
            for item in data["tracks"]:
                track = Track(
                    id=item["id"],
                    name=item["name"],
                    artists=[{"id": a["id"], "name": a["name"]} for a in item["artists"]],
                    album={
                        "id": item["album"]["id"],
                        "name": item["album"]["name"],
                        "images": item["album"]["images"]
                    },
                    duration_ms=item["duration_ms"],
                    preview_url=item.get("preview_url"),
                    external_urls=item["external_urls"]
                )
                tracks.append(track)
            
            return tracks
    
    async def search_tracks(
        self,
        access_token: str,
        query: str,
        limit: int = 10,
        market: str = "US"
    ) -> List[Track]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_base_url}/search",
                headers=self._get_headers(access_token),
                params={"q": query, "type": "track", "limit": limit, "market": market}
            )
            response.raise_for_status()
            data = response.json()
            
            tracks = []
            for item in data.get("tracks", {}).get("items", []):
                track = Track(
                    id=item["id"],
                    name=item["name"],
                    artists=[{"id": a["id"], "name": a["name"]} for a in item["artists"]],
                    album={
                        "id": item["album"]["id"],
                        "name": item["album"]["name"],
                        "images": item["album"]["images"]
                    },
                    duration_ms=item["duration_ms"],
                    preview_url=item.get("preview_url"),
                    external_urls=item["external_urls"]
                )
                tracks.append(track)
            
            return tracks
    
    async def create_playlist(
        self,
        access_token: str,
        user_id: str,
        name: str,
        description: Optional[str] = None,
        public: bool = False
    ) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base_url}/users/{user_id}/playlists",
                headers=self._get_headers(access_token),
                json={
                    "name": name,
                    "description": description or "",
                    "public": public
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def add_tracks_to_playlist(
        self,
        access_token: str,
        playlist_id: str,
        track_uris: List[str]
    ) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base_url}/playlists/{playlist_id}/tracks",
                headers=self._get_headers(access_token),
                json={"uris": track_uris}
            )
            response.raise_for_status()
            return response.json()
