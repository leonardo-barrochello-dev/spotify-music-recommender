You are a senior AI engineer and full-stack developer. Your task is to build a production-ready music recommendation system using the Spotify API.

## 🎯 Project Goal
Create a full-stack application that recommends music based on user preferences using Spotify OAuth authentication and a machine learning similarity model built with TensorFlow.

---

## 🧠 Core Requirements

### 1. Authentication
- Implement OAuth 2.0 with the Spotify Web API
- Allow users to log in with their Spotify account
- Store access and refresh tokens securely
- Use scopes:
  - user-read-private
  - user-read-email
  - user-top-read
  - playlist-modify-public
  - playlist-modify-private

---

### 2. Data Collection
- Fetch:
  - User's top tracks
  - User's top artists
- Retrieve audio features for tracks:
  - danceability
  - energy
  - valence
  - tempo
  - acousticness
  - instrumentalness

---

### 3. Feature Engineering
- Represent each track as a feature vector
- Build a user vector by averaging the vectors of top tracks
- Normalize features before processing

---

### 4. Machine Learning (TensorFlow)
- Use TensorFlow (NOT sklearn) to:
  - Compute similarity using vector operations (dot product / cosine similarity)
- Build a simple ranking function:
  score = similarity(user_vector, item_vector)

- Efficiently compute similarity against a batch of candidate tracks

---

### 5. Candidate Generation
- Use Spotify endpoints to get:
  - Related artists
  - Top tracks from those artists
- Build a candidate pool of tracks

---

### 6. Ranking
- Rank candidate tracks using similarity score
- Return top N recommendations

---

### 7. Backend (FastAPI)
- Build REST API with endpoints:
  - /auth/login
  - /auth/callback
  - /user/profile
  - /recommendations
  - /playlist/create

- Handle token refresh automatically
- Structure code with services:
  - spotify_service
  - recommendation_service
  - auth_service

---

### 8. Frontend (React)
- Build a UI inspired by Spotify:
  - Dark theme
  - Sidebar navigation
  - Music cards (album cover, title, artist)

### Features:
- Login with Spotify
- Show user's top tracks
- Show recommendations
- Button: "Add to Spotify Playlist"
- Button: "Play on Spotify"

---

### 9. Playlist Integration
- Allow user to:
  - Create a playlist in their Spotify account
  - Add recommended tracks directly via API

---

### 10. Architecture
- Clean architecture:
  - separation of concerns
  - services, controllers, models

- Use environment variables for secrets

---

### 11. Tech Stack
- Backend: FastAPI (Python)
- ML: TensorFlow
- Frontend: React + modern UI (Tailwind or similar)
- HTTP: Axios or Fetch
- Auth: Spotify OAuth 2.0

---

### 12. Bonus Features (if possible)
- Mood filter (happy, chill, workout)
- Explanation of recommendations
- Loading states and error handling
- Caching results for performance

---

## 📦 Deliverables

- Full backend project
- Full frontend project
- Clear folder structure
- Requirements.txt / package.json
- Instructions to run locally
- .env.example file

---

## ⚠️ Important Constraints

- Do NOT use scikit-learn for similarity
- Use TensorFlow operations for vector math
- Code must be clean, modular, and readable
- Avoid hardcoding values
- Follow best practices for API design

---

## 🎯 Expected Outcome

A working full-stack application where:
- User logs in with Spotify
- System fetches their preferences
- Recommends songs using vector similarity
- User can add songs directly to their Spotify account
