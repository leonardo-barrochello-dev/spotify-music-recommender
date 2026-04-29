@echo off
echo ========================================
echo  Spotify Music Recommender - Setup
echo ========================================
echo.

echo [1/4] Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

echo Copying environment file...
if not exist .env copy .env.example .env

echo.
echo [2/4] Setting up Frontend...
cd ..\frontend

echo Installing Node dependencies...
call npm install

echo Copying environment file...
if not exist .env copy .env.example .env

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Edit backend\.env with your Spotify credentials:
echo    - SPOTIFY_CLIENT_ID
echo    - SPOTIFY_CLIENT_SECRET
echo.
echo 2. Start the backend:
echo    cd backend
echo    venv\Scripts\activate
echo    uvicorn app.main:app --reload
echo.
echo 3. Start the frontend (new terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open http://localhost:5173
echo.
echo ========================================
