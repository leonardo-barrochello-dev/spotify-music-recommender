from fastapi import APIRouter, Depends, Query
from app.services.spotify_service import SpotifyService
from app.dependencies import get_current_user, get_spotify_token
from app.models.schemas import UserProfileResponse, User, Track, Artist
from typing import List

router = APIRouter()

spotify_service = SpotifyService()


@router.get("/profile", response_model=User)
async def get_profile(
    access_token: str = Depends(get_spotify_token),
    current_user: dict = Depends(get_current_user)
):
    try:
        print(f"[UserRouter] Fetching profile for user: {current_user.get('spotify_user_id')}")
        user = await spotify_service.get_current_user(access_token)
        return user
    except Exception as e:
        print(f"[UserRouter] Error fetching profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch profile: {str(e)}")


@router.get("/top-tracks", response_model=List[Track])
async def get_top_tracks(
    access_token: str = Depends(get_spotify_token),
    limit: int = Query(default=20, ge=1, le=50),
    time_range: str = Query(default="medium_term", description="short_term, medium_term, or long_term")
):
    try:
        print(f"[UserRouter] Fetching top tracks: limit={limit}, range={time_range}")
        tracks = await spotify_service.get_top_tracks(
            access_token=access_token,
            limit=limit,
            time_range=time_range
        )
        
        if not tracks:
            print("[UserRouter] No top tracks found")
            return []
            
        track_ids = [track.id for track in tracks]
        print(f"[UserRouter] Fetching audio features for {len(track_ids)} tracks")
        
        try:
            audio_features = await spotify_service.get_audio_features(access_token, track_ids)
            for track in tracks:
                if track.id in audio_features:
                    track.audio_features = audio_features[track.id]
        except Exception as fe:
            print(f"[UserRouter] Error fetching audio features (non-critical): {str(fe)}")
            # Continuar mesmo sem audio features
        
        return tracks
    except Exception as e:
        print(f"[UserRouter] Error in get_top_tracks: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to fetch top tracks: {str(e)}")


@router.get("/top-artists", response_model=List[Artist])
async def get_top_artists(
    access_token: str = Depends(get_spotify_token),
    limit: int = Query(default=20, ge=1, le=50),
    time_range: str = Query(default="medium_term", description="short_term, medium_term, or long_term")
):
    artists = await spotify_service.get_top_artists(
        access_token=access_token,
        limit=limit,
        time_range=time_range
    )
    return artists


@router.get("/profile/full", response_model=UserProfileResponse)
async def get_full_profile(
    access_token: str = Depends(get_spotify_token),
    current_user: dict = Depends(get_current_user)
):
    user = await spotify_service.get_current_user(access_token)
    top_tracks = await spotify_service.get_top_tracks(access_token, limit=20)
    top_artists = await spotify_service.get_top_artists(access_token, limit=20)
    
    track_ids = [track.id for track in top_tracks]
    audio_features = await spotify_service.get_audio_features(access_token, track_ids)
    
    for track in top_tracks:
        if track.id in audio_features:
            track.audio_features = audio_features[track.id]
    
    return UserProfileResponse(
        user=user,
        top_tracks=top_tracks,
        top_artists=top_artists
    )
