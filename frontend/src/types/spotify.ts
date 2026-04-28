export interface SpotifyUser {
  id: string;
  email: string;
  display_name: string;
  images?: Array<{
    url: string;
    height: number;
    width: number;
  }>;
  country?: string;
  product?: string;
}

export interface SpotifyArtist {
  id: string;
  name: string;
  genres?: string[];
  images?: Array<{
    url: string;
    height: number;
    width: number;
  }>;
  external_urls?: {
    spotify: string;
  };
}

export interface SpotifyAlbum {
  id: string;
  name: string;
  images?: Array<{
    url: string;
    height: number;
    width: number;
  }>;
}

export interface SpotifyAudioFeatures {
  danceability: number;
  energy: number;
  valence: number;
  tempo: number;
  acousticness: number;
  instrumentalness: number;
  liveness: number;
  loudness: number;
  speechiness: number;
  duration_ms: number;
  time_signature: number;
  key: number;
  mode: number;
}

export interface SpotifyTrack {
  id: string;
  name: string;
  artists: SpotifyArtist[];
  album: SpotifyAlbum;
  duration_ms: number;
  preview_url?: string | null;
  external_urls?: {
    spotify: string;
  };
  audio_features?: SpotifyAudioFeatures;
}

export interface RecommendationResponse {
  tracks: SpotifyTrack[];
  user_vector?: number[];
  explanation?: string;
}

export interface PlaylistCreateRequest {
  name: string;
  description?: string;
  track_uris: string[];
}

export interface PlaylistCreateResponse {
  playlist_id: string;
  playlist_url: string;
  tracks_added: number;
}

export interface UserProfileResponse {
  user: SpotifyUser;
  top_tracks: SpotifyTrack[];
  top_artists: SpotifyArtist[];
}

export interface MoodOption {
  value: string;
  label: string;
  description: string;
}

export interface TimeRangeOption {
  value: string;
  label: string;
}
