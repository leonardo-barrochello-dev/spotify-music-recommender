import api from './api';
import type { SpotifyTrack, SpotifyArtist, SpotifyUser, RecommendationResponse, PlaylistCreateResponse, PlaylistCreateRequest, UserProfileResponse } from '../types/spotify';

export const userService = {
  getProfile: async (): Promise<SpotifyUser> => {
    const response = await api.get<SpotifyUser>('/user/profile');
    return response.data;
  },

  getFullProfile: async (): Promise<UserProfileResponse> => {
    const response = await api.get<UserProfileResponse>('/user/profile/full');
    return response.data;
  },

  getTopTracks: async (limit = 20, timeRange = 'medium_term'): Promise<SpotifyTrack[]> => {
    const response = await api.get<SpotifyTrack[]>('/user/top-tracks', {
      params: { limit, time_range: timeRange },
    });
    return response.data;
  },

  getTopArtists: async (limit = 20, timeRange = 'medium_term'): Promise<SpotifyArtist[]> => {
    const response = await api.get<SpotifyArtist[]>('/user/top-artists', {
      params: { limit, time_range: timeRange },
    });
    return response.data;
  },
};

export const recommendationService = {
  getRecommendations: async (limit = 20, mood: string | null = null): Promise<RecommendationResponse> => {
    const params: Record<string, string | number> = { limit };
    if (mood) params.mood = mood;
    const response = await api.get<RecommendationResponse>('/recommendations/', { params });
    return response.data;
  },

  createPlaylist: async (name: string, description = '', trackUris: string[] = []): Promise<PlaylistCreateResponse> => {
    const payload: PlaylistCreateRequest = {
      name,
      description,
      track_uris: trackUris,
    };
    const response = await api.post<PlaylistCreateResponse>('/recommendations/playlist/create', payload);
    return response.data;
  },

  createPlaylistFromRecommendations: async (
    limit = 20,
    mood: string | null = null,
    playlistName: string | null = null
  ): Promise<PlaylistCreateResponse> => {
    const params: Record<string, string | number | null> = { limit, mood, playlist_name: playlistName };
    const response = await api.post<PlaylistCreateResponse>(
      '/recommendations/playlist/from-recommendations',
      null,
      { params }
    );
    return response.data;
  },
};
