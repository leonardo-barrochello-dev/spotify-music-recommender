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
from typing import List

router = APIRouter()

spotify_service = SpotifyService()
recommendation_engine = RecommendationEngine()


@router.get("/", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest = Depends(),
    access_token: str = Depends(get_spotify_token),
    current_user: dict = Depends(get_current_user)
):
    try:
        top_tracks = await spotify_service.get_top_tracks(access_token, limit=20)
        top_artists = await spotify_service.get_top_artists(access_token, limit=5)
        
        if not top_tracks:
            raise HTTPException(status_code=400, detail="No top tracks found to build preferences")
        
        track_ids = [track.id for track in top_tracks]
        audio_features = await spotify_service.get_audio_features(access_token, track_ids)
        
        tracks_with_features = [t for t in top_tracks if t.id in audio_features]
        if not tracks_with_features:
            raise HTTPException(status_code=400, detail="Could not fetch audio features")
        
        candidate_tracks = []
        for artist in top_artists[:3]:
            related_artists = await spotify_service.get_related_artists(access_token, artist.id)
            for related_artist in related_artists[:5]:
                artist_tracks = await spotify_service.get_artist_top_tracks(access_token, related_artist.id)
                candidate_tracks.extend(artist_tracks)
        
        known_track_ids = set(track_ids)
        candidate_tracks = [t for t in candidate_tracks if t.id not in known_track_ids]
        
        candidate_ids = list(set([t.id for t in candidate_tracks]))
        candidate_audio_features = await spotify_service.get_audio_features(access_token, candidate_ids)
        
        for track in candidate_tracks:
            if track.id in candidate_audio_features:
                track.audio_features = candidate_audio_features[track.id]
        
        candidate_tracks = [t for t in candidate_tracks if t.audio_features]
        
        recommended_tracks, user_vector, explanation = recommendation_engine.generate_recommendations(
            user_tracks=tracks_with_features,
            candidate_tracks=candidate_tracks,
            limit=request.limit,
            mood=request.mood
        )
        
        return RecommendationResponse(
            tracks=recommended_tracks,
            user_vector=user_vector,
            explanation=explanation
        )
        
    except Exception as e:
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
