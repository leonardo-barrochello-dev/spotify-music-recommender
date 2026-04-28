# 🚀 Quick Start Guide

## 1. Configure Spotify Credentials

Edit `backend\.env` with your Spotify app credentials:

```env
SPOTIFY_CLIENT_ID=your_actual_client_id_here
SPOTIFY_CLIENT_SECRET=your_actual_client_secret_here
```

**Get your credentials:**
1. Go to https://developer.spotify.com/dashboard
2. Create an app (if you haven't)
3. Copy Client ID and Client Secret
4. Make sure Redirect URI is: `http://127.0.0.1:8000/auth/callback`

## 2. Start the Application

### Option A: Using Batch Scripts (Windows)

**Terminal 1 - Backend:**
```bash
start-backend.bat
```

**Terminal 2 - Frontend:**
```bash
start-frontend.bat
```

### Option B: Manual Commands

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## 3. Access the App

- **Frontend:** http://localhost:5173
- **Backend API:** http://127.0.0.1:8000
- **API Docs:** http://127.0.0.1:8000/docs

## 4. Test the Flow

1. Click "Login with Spotify"
2. Authorize the app
3. View your top tracks on Dashboard
4. Go to Recommendations
5. Select a mood filter
6. Create a playlist with recommended tracks

## Troubleshooting

### Backend won't start
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt --force-reinstall
```

### Frontend won't connect
- Make sure backend is running on port 8000
- Clear browser localStorage
- Check CORS settings in `backend/app/main.py`

### Authentication fails
- Verify Client ID and Secret in `backend\.env`
- Check Redirect URI matches exactly in Spotify Dashboard
- Ensure no extra spaces in .env values

## Need Help?

Check the full README.md for detailed documentation.
