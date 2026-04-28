from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from app.services.auth_service import AuthService
from app.services.spotify_service import SpotifyService
from app.services.token_service import token_service
from app.config import settings
import secrets

router = APIRouter()

auth_service = AuthService()
spotify_service = SpotifyService()


@router.get("/login")
async def login():
    state = secrets.token_urlsafe(16)
    authorization_url = auth_service.get_authorization_url(state)
    
    response = RedirectResponse(url=authorization_url)
    response.set_cookie(key="oauth_state", value=state, httponly=True, max_age=600)
    
    return response


@router.get("/callback")
async def callback(
    request: Request,
    code: str = Query(None),
    error: str = Query(None),
    state: str = Query(None)
):
    print(f"[Auth Callback] Received - code: {code[:10] if code else None}..., error: {error}, state: {state}")
    
    if error:
        print(f"[Auth Callback] Error from Spotify: {error}")
        raise HTTPException(status_code=400, detail=f"Spotify auth error: {error}")
    
    if not code:
        print("[Auth Callback] No code provided")
        raise HTTPException(status_code=400, detail="No authorization code provided")
    
    oauth_state = request.cookies.get("oauth_state")
    print(f"[Auth Callback] OAuth state from cookie: {oauth_state}, matches: {oauth_state == state}")
    
    if not oauth_state or oauth_state != state:
        print("[Auth Callback] Invalid state parameter")
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    
    try:
        print("[Auth Callback] Exchanging code for token...")
        spotify_token = await auth_service.exchange_code_for_token(code)
        print(f"[Auth Callback] Token received, expires in: {spotify_token.expires_in}s")
        
        spotify_service_instance = SpotifyService()
        print("[Auth Callback] Fetching user profile...")
        user = await spotify_service_instance.get_current_user(spotify_token.access_token)
        print(f"[Auth Callback] User profile fetched for: {user.spotify_user_id}")
        
        print("[Auth Callback] Creating session token...")
        session_token = token_service.create_session_token(
            spotify_user_id=user.spotify_user_id,
            spotify_token=spotify_token
        )
        print(f"[Auth Callback] Session created: {session_token[:10]}...")
        
        redirect_url = f"{settings.FRONTEND_URL}/login?session_token={session_token}"
        print(f"[Auth Callback] FINAL REDIRECT TO: {redirect_url}")
        
        response = RedirectResponse(url=redirect_url)
        response.delete_cookie(key="oauth_state")
        
        return response
        
    except Exception as e:
        print(f"[Auth Callback] !!! CRITICAL ERROR !!!: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": "Authentication failed", "details": str(e)}
        )


@router.get("/logout")
async def logout(session_token: str = Query(None)):
    if session_token:
        token_service.invalidate_session(session_token)
    
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie(key="session_token")
    
    return response
