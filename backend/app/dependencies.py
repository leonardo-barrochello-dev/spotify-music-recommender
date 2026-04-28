from fastapi import Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from app.services.token_service import token_service
from app.services.auth_service import AuthService
from app.config import settings
from typing import Optional

auth_service = AuthService()


async def get_session_token(request: Request) -> Optional[str]:
    session_token = request.cookies.get("session_token")
    if not session_token:
        session_token = request.query_params.get("session_token")
    return session_token


async def get_current_user(
    session_token: Optional[str] = Depends(get_session_token)
) -> dict:
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_data = token_service.validate_session_token(session_token)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_data


async def get_spotify_token(
    current_user: dict = Depends(get_current_user)
) -> str:
    spotify_user_id = current_user["spotify_user_id"]
    print(f"[Dependencies] Getting Spotify token for user: {spotify_user_id}")
    
    spotify_token = token_service.get_spotify_token(spotify_user_id)
    
    if spotify_token:
        print(f"[Dependencies] Found valid Spotify token for: {spotify_user_id}")
        return spotify_token
    
    # Token expirado ou não encontrado, tentar fazer refresh
    print(f"[Dependencies] Token not found, attempting refresh...")
    refresh_token = token_service.get_refresh_token(spotify_user_id)
    
    if refresh_token:
        print(f"[Dependencies] Found refresh token, exchanging...")
        try:
            new_token = await auth_service.refresh_access_token(refresh_token)
            token_service.update_spotify_token(spotify_user_id, new_token)
            print(f"[Dependencies] Token refreshed successfully for: {spotify_user_id}")
            return new_token.access_token
        except Exception as e:
            print(f"[Dependencies] Failed to refresh token: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="SESSION_EXPIRED",
            )
    else:
        print(f"[Dependencies] No refresh token found for: {spotify_user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="SESSION_EXPIRED",
        )
