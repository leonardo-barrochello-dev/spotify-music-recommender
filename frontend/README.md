# Spotify Music Recommender - Frontend

React + TypeScript + Vite frontend for the Spotify Music Recommendation System.

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS 3** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at:
- **Frontend:** http://localhost:5173

## Project Structure

```
frontend/
├── src/
│   ├── App.tsx                 # Main app with routing
│   ├── main.tsx               # Entry point
│   ├── index.css              # Global styles + Tailwind
│   ├── vite-env.d.ts          # TypeScript declarations
│   ├── types/
│   │   └── spotify.ts         # Spotify API types
│   ├── components/
│   │   ├── Layout/
│   │   │   ├── Layout.tsx     # Main layout wrapper
│   │   │   └── Header.tsx     # Top navigation
│   │   ├── Sidebar/
│   │   │   └── Sidebar.tsx    # Navigation sidebar
│   │   ├── TrackCard/
│   │   │   └── TrackCard.tsx  # Track display card
│   │   └── PlaylistModal/
│   │       └── PlaylistModal.tsx # Create playlist modal
│   ├── pages/
│   │   ├── Login/
│   │   │   └── Login.tsx      # Login page
│   │   ├── Dashboard/
│   │   │   └── Dashboard.tsx  # User dashboard
│   │   └── Recommendations/
│   │       └── Recommendations.tsx # Recommendations page
│   ├── services/
│   │   ├── api.ts             # Axios instance
│   │   └── musicService.ts    # API service functions
│   ├── hooks/
│   │   └── useAuth.tsx        # Auth context
│   └── utils/
│       └── constants.ts       # App constants
├── package.json
├── tsconfig.json
├── tsconfig.node.json
├── vite.config.ts
├── tailwind.config.ts
├── postcss.config.js
└── .env.example
```

## Available Scripts

```bash
npm run dev      # Start development server (http://localhost:5173)
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Lint code with ESLint
```

## Type Safety

All components and services are fully typed with TypeScript:

- **Spotify API types** in `src/types/spotify.ts`
- **Strict mode** enabled in `tsconfig.json`
- **Type inference** for React hooks and props
- **No `any` types** used (except where absolutely necessary)

## Features

- ✅ **Login with Spotify** - OAuth2 authentication
- ✅ **Dashboard** - View top tracks and artists
- ✅ **Recommendations** - AI-powered music suggestions
- ✅ **Mood Filters** - happy, chill, workout, sad, energetic
- ✅ **Create Playlists** - Add tracks to Spotify
- ✅ **Dark Theme** - Spotify-inspired UI
- ✅ **TypeScript** - Full type safety
- ✅ **Responsive** - Works on all screen sizes

## API Integration

All API calls go through the backend:

- **Base URL:** `http://127.0.0.1:8000`
- **Session token:** Passed via query params
- **Auto-redirect:** On 401 errors

Example usage:

```typescript
import { userService } from './services/musicService';

// Get user profile
const profile = await userService.getProfile();

// Get top tracks
const tracks = await userService.getTopTracks(20, 'medium_term');

// Get recommendations
const { recommendationService } = await import('./services/musicService');
const recs = await recommendationService.getRecommendations(20, 'happy');
```

## Authentication Flow

1. User clicks "Login with Spotify"
2. Redirected to backend: `/auth/login`
3. User authorizes on Spotify
4. Backend redirects back with `session_token`
5. Token stored in `localStorage`
6. User authenticated, redirected to `/dashboard`

## Tailwind CSS

Custom Spotify color palette configured in `tailwind.config.ts`:

```typescript
colors: {
  spotify: {
    green: '#1DB954',
    black: '#191414',
    darkGray: '#282828',
    lightGray: '#B3B3B3',
    white: '#FFFFFF',
    darkerGray: '#181818',
    cardGray: '#121212'
  }
}
```

## Build for Production

```bash
npm run build
```

Output will be in the `dist/` folder.

Preview the production build:

```bash
npm run preview
```
