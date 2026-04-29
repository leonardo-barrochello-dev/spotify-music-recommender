from fastapi import APIRouter, Depends, HTTPException
from app.services.spotify_service import SpotifyService
from app.dependencies import get_current_user, get_spotify_token
from app.models.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    PlaylistCreateRequest,
    PlaylistCreateResponse,
    Track
)
from app.ml.recommendation_engine import RecommendationEngine
from app.ml.candidate_generator import CandidateGenerator
from app.utils.cache import (
    get_redis_client,
    cache_get,
    cache_setex,
    cache_delete,
    serialize_tracks,
    deserialize_tracks,
    serialize_artists,
    deserialize_artists
)
from app.enums import SearchType
from typing import List, Optional
import traceback
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter()

spotify_service = SpotifyService()
recommendation_engine = RecommendationEngine()
candidate_generator = CandidateGenerator(spotify_service)


@router.get("/", response_model=RecommendationResponse)
async def get_recommendations(
    limit: int = 20,
    mood: Optional[str] = None,
    refresh: bool = False,
    access_token: str = Depends(get_spotify_token),
    current_user: dict = Depends(get_current_user)
):
    request = RecommendationRequest(limit=limit, mood=mood)
    try:
        user_id = current_user["spotify_user_id"]
        logger.info(f"Getting recommendations for user: {user_id}, limit={limit}, mood={mood}, refresh={refresh}")

        redis_client = get_redis_client()
        spotify_calls_avoided = 0

        if refresh and redis_client:
            cache_keys = [
                f"user:{user_id}:top_tracks",
                f"user:{user_id}:top_artists",
                f"user:{user_id}:candidates"
            ]
            for key in cache_keys:
                redis_client.delete(key)
            logger.info(f"Cache cleared for user {user_id} (refresh requested)")

        cache_key_tracks = f"user:{user_id}:top_tracks"
        if redis_client:
            cached = cache_get(cache_key_tracks)
            if cached:
                top_tracks = deserialize_tracks(cached)
                spotify_calls_avoided += 1
                logger.info(f"Cache HIT: top_tracks for user {user_id}")
            else:
                top_tracks = await spotify_service.get_top_tracks(access_token, limit=20)
                cache_setex(cache_key_tracks, 600, serialize_tracks(top_tracks))
                logger.info(f"Cache MISS: fetched and cached top_tracks for user {user_id}")
        else:
            top_tracks = await spotify_service.get_top_tracks(access_token, limit=20)

        cache_key_artists = f"user:{user_id}:top_artists"
        if redis_client:
            cached = cache_get(cache_key_artists)
            if cached:
                top_artists = deserialize_artists(cached)
                spotify_calls_avoided += 1
                logger.info(f"Cache HIT: top_artists for user {user_id}")
            else:
                top_artists = await spotify_service.get_top_artists(access_token, limit=5)
                cache_setex(cache_key_artists, 600, serialize_artists(top_artists))
                logger.info(f"Cache MISS: fetched and cached top_artists for user {user_id}")
        else:
            top_artists = await spotify_service.get_top_artists(access_token, limit=5)

        if not top_tracks:
            raise HTTPException(status_code=400, detail="No top tracks found to build preferences")

        logger.info(f"User has {len(top_tracks)} top tracks and {len(top_artists)} top artists")
        logger.info(f"Spotify API calls avoided: {spotify_calls_avoided}")

        genres = set()
        for artist in top_artists:
            genres.update(artist.genres[:2])

        genres_list = list(genres)[:5]
        logger.info(f"User genres: {genres_list}")

        cache_key_candidates = f"user:{user_id}:candidates"
        if redis_client:
            cached = cache_get(cache_key_candidates)
            if cached:
                candidate_tracks = deserialize_tracks(cached["tracks"])
                candidate_scores = cached["scores"]
                logger.info(f"Cache HIT: candidates for user {user_id} ({len(candidate_tracks)} tracks)")
            else:
                candidate_tracks, candidate_scores = await candidate_generator.generate(
                    top_tracks=top_tracks,
                    top_artists=top_artists,
                    access_token=access_token
                )
                cache_setex(
                    cache_key_candidates,
                    600,
                    {
                        "tracks": serialize_tracks(candidate_tracks),
                        "scores": candidate_scores
                    }
                )
                logger.info(f"Cache MISS: generated and cached candidates for user {user_id} ({len(candidate_tracks)} tracks)")
        else:
            candidate_tracks, candidate_scores = await candidate_generator.generate(
                top_tracks=top_tracks,
                top_artists=top_artists,
                access_token=access_token
            )

        if not candidate_tracks:
            logger.warning("No candidates generated, using exploration queries")
            for query in ["rock", "pop", "electronic", "hip-hop"]:
                try:
                    tracks = await spotify_service.search(access_token, type=SearchType.TRACK, query=query, limit=10)
                    candidate_tracks.extend(tracks)
                except Exception as e:
                    logger.warning(f"Exploration search failed: {e}")
            candidate_scores = {}

        known_track_ids = {t.id for t in top_tracks}
        candidate_tracks = [t for t in candidate_tracks if t.id not in known_track_ids]

        logger.info(f"Found {len(candidate_tracks)} candidate tracks before ranking")

        recommended_tracks = recommendation_engine.rank_tracks(
            user_tracks=top_tracks,
            candidate_tracks=candidate_tracks,
            candidate_scores=candidate_scores,
            limit=limit,
            mood=mood
        )

        logger.info(f"Returning {len(recommended_tracks)} recommended tracks")

        explanation = f"Based on your top {len(top_tracks)} tracks"
        if genres_list:
            explanation += f" and genres like {', '.join(genres_list)}"
        if mood:
            explanation += f" with a {mood} mood"

        return RecommendationResponse(
            tracks=recommended_tracks,
            user_vector=None,
            explanation=explanation
        )

    except Exception as e:
        logger.error(f"Error generating recommendations: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")


@router.post("/playlist/create", response_model=PlaylistCreateResponse)
async def create_playlist(
    playlist_request: PlaylistCreateRequest,
    access_token: str = Depends(get_spotify_token),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user["spotify_user_id"]
        
        playlist_data = await spotify_service.create_playlist(
            access_token=access_token,
            user_id=user_id,
            name=playlist_request.name,
            description=playlist_request.description,
            public=False
        )
        
        playlist_id = playlist_data["id"]
        
        if playlist_request.track_uris:
            tracks_to_add = playlist_request.track_uris[:100]
            await spotify_service.add_tracks_to_playlist(
                access_token=access_token,
                playlist_id=playlist_id,
                track_uris=tracks_to_add
            )
        
        return PlaylistCreateResponse(
            playlist_id=playlist_id,
            playlist_url=playlist_data["external_urls"]["spotify"],
            tracks_added=len(playlist_request.track_uris)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create playlist: {str(e)}")


@router.post("/playlist/from-recommendations", response_model=PlaylistCreateResponse)
async def create_playlist_from_recommendations(
    request: RecommendationRequest,
    playlist_name: str = None,
    access_token: str = Depends(get_spotify_token),
    current_user: dict = Depends(get_current_user)
):
    try:
        recommendations = await get_recommendations(
            request=request,
            access_token=access_token,
            current_user=current_user
        )
        
        track_uris = [f"spotify:track:{track.id}" for track in recommendations.tracks]
        
        playlist_name = playlist_name or f"Recommended for You - {request.mood or 'Mix'}"
        
        playlist_request = PlaylistCreateRequest(
            name=playlist_name,
            description=f"Generated by Spotify Music Recommender based on your {request.mood or 'listening'} preferences",
            track_uris=track_uris
        )
        
        return await create_playlist(
            playlist_request=playlist_request,
            access_token=access_token,
            current_user=current_user
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create playlist from recommendations: {str(e)}")
