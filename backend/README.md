# Spotify Music Recommender - Backend

FastAPI backend for the Spotify Music Recommendation System.

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your Spotify credentials:

```bash
copy .env.example .env
```

Edit `.env` with your values:
```env
SPOTIFY_CLIENT_ID=your_client_id_from_spotify_dashboard
SPOTIFY_CLIENT_SECRET=your_client_secret_from_spotify_dashboard
REDIRECT_URI=http://127.0.0.1:8000/auth/callback
FRONTEND_URL=http://localhost:5173
SECRET_KEY=your_random_secret_key_for_sessions
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## API Endpoints

### Authentication
- `GET /auth/login` - Redirect to Spotify OAuth
- `GET /auth/callback` - OAuth callback handler
- `GET /auth/logout` - Logout user

### User
- `GET /user/profile` - Get user profile
- `GET /user/top-tracks` - Get user's top tracks
- `GET /user/top-artists` - Get user's top artists
- `GET /user/profile/full` - Get complete profile with top tracks and artists

### Recommendations
- `GET /recommendations/?limit=20&mood=happy` - Get music recommendations
- `POST /recommendations/playlist/create` - Create playlist with tracks
- `POST /recommendations/playlist/from-recommendations` - Create playlist from recommendations

## Testing

### Test Health Endpoint
```bash
curl http://127.0.0.1:8000/health
```

### Test Login Flow
1. Open browser to `http://127.0.0.1:8000/auth/login`
2. Authorize with Spotify
3. You'll be redirected to frontend with session token

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Pydantic settings
│   ├── dependencies.py         # FastAPI dependencies
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   ├── services/
│   │   ├── auth_service.py     # OAuth2 authentication
│   │   ├── spotify_service.py  # Spotify API wrapper
│   │   └── token_service.py    # Token management
│   ├── routers/
│   │   ├── auth.py             # Auth endpoints
│   │   ├── user.py             # User endpoints
│   │   └── recommendations.py  # Recommendation endpoints
│   ├── ml/
│   │   ├── feature_engineering.py  # Feature extraction
│   │   ├── similarity_model.py     # TensorFlow similarity
│   │   └── recommendation_engine.py # ML pipeline
│   └── utils/
│       └── security.py         # Security utilities
├── requirements.txt
└── .env.example
```

## ML Model

The recommendation engine uses:
- **TensorFlow** for cosine similarity computation
- **Feature vector**: 6 dimensions (danceability, energy, valence, tempo, acousticness, instrumentalness)
- **Candidate generation**: Related artists from user's top artists
- **Ranking**: Cosine similarity between user vector and candidate tracks

## Mood Filters

Available mood options for recommendations:
- `happy` - Upbeat and positive vibes
- `chill` - Relaxed and mellow atmosphere
- `workout` - High-energy beats
- `sad` - Emotional and introspective tones
- `energetic` - Dynamic and powerful rhythms
