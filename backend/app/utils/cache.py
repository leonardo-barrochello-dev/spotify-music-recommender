import redis
import json
import logging
from typing import Optional, List, Dict, Any
from app.config import settings
from app.models.schemas import Track, Artist

logger = logging.getLogger(__name__)

_redis_client: Optional[redis.Redis] = None
_redis_available: bool = False


def get_redis_client() -> Optional[redis.Redis]:
    global _redis_client, _redis_available

    if not settings.REDIS_ENABLED:
        return None

    if _redis_client is not None:
        if _redis_available:
            return _redis_client
        return None

    try:
        _redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2
        )
        _redis_client.ping()
        _redis_available = True
        logger.info(f"Redis connected at {settings.REDIS_HOST}:{settings.REDIS_PORT}")
        return _redis_client
    except Exception as e:
        _redis_available = False
        logger.warning(f"Redis unavailable, continuing without cache: {e}")
        return None


def cache_get(key: str) -> Optional[Any]:
    client = get_redis_client()
    if not client:
        return None
    try:
        value = client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        logger.warning(f"Cache get failed for key {key}: {e}")
        return None


def cache_setex(key: str, ttl: int, value: Any) -> bool:
    client = get_redis_client()
    if not client:
        return False
    try:
        client.setex(key, ttl, json.dumps(value))
        return True
    except Exception as e:
        logger.warning(f"Cache set failed for key {key}: {e}")
        return False


def cache_delete(key: str) -> bool:
    client = get_redis_client()
    if not client:
        return False
    try:
        client.delete(key)
        return True
    except Exception as e:
        logger.warning(f"Cache delete failed for key {key}: {e}")
        return False


def serialize_tracks(tracks: List[Track]) -> List[Dict[str, Any]]:
    return [track.model_dump() for track in tracks]


def deserialize_tracks(data: List[Dict[str, Any]]) -> List[Track]:
    return [Track(**item) for item in data]


def serialize_artists(artists: List[Artist]) -> List[Dict[str, Any]]:
    return [artist.model_dump() for artist in artists]


def deserialize_artists(data: List[Dict[str, Any]]) -> List[Artist]:
    return [Artist(**item) for item in data]
