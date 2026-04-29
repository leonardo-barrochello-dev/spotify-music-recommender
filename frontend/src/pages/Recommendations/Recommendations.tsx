import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../../components/Layout/Layout';
import TrackCard from '../../components/TrackCard/TrackCard';
import PlaylistModal from '../../components/PlaylistModal/PlaylistModal';
import { useAuth } from '../../hooks/useAuth';
import { recommendationService } from '../../services/musicService';
import { MOOD_OPTIONS } from '../../utils/constants';
import type { SpotifyTrack } from '../../types/spotify';

export default function Recommendations() {
  const { isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState<SpotifyTrack[]>([]);
  const [selectedMood, setSelectedMood] = useState('');
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  const [showPlaylistModal, setShowPlaylistModal] = useState(false);
  const [userVector, setUserVector] = useState<number[] | null>(null);
  const [explanation, setExplanation] = useState('');

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, loading, navigate]);

  const loadRecommendations = async (mood = '') => {
    setLoadingRecommendations(true);
    try {
      const data = await recommendationService.getRecommendations(50, mood || null);
      setRecommendations(data.tracks || []);
      setUserVector(data.user_vector || null);
      setExplanation(data.explanation || '');
    } catch (error) {
      console.error('Failed to load recommendations:', error);
      alert('Failed to load recommendations. Please try again.');
    } finally {
      setLoadingRecommendations(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      loadRecommendations(selectedMood);
    }
  }, [isAuthenticated]);

  const handleMoodChange = (mood: string) => {
    setSelectedMood(mood);
    loadRecommendations(mood);
  };

  const handlePlayTrack = (track: SpotifyTrack) => {
    window.open(track.external_urls?.spotify, '_blank');
  };

  const handleCreatePlaylist = async (name: string, description: string, trackUris: string[]) => {
    try {
      const result = await recommendationService.createPlaylist(
        name,
        description,
        trackUris
      );
      alert(`Playlist "${result.playlist_id}" created successfully!`);
      window.open(result.playlist_url, '_blank');
      setShowPlaylistModal(false);
    } catch (error) {
      console.error('Failed to create playlist:', error);
      alert('Failed to create playlist. Please try again.');
      throw error;
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full">
          <div className="text-spotify-lightGray">Loading...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">
            Recommendations
          </h1>
          <p className="text-spotify-lightGray">
            Discover new music tailored to your taste
          </p>
        </div>

        <div>
          <h2 className="text-xl font-semibold text-white mb-3">
            Select a Mood
          </h2>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => handleMoodChange('')}
              className={`px-5 py-2 rounded-full font-semibold transition-all ${selectedMood === ''
                  ? 'bg-spotify-green text-black'
                  : 'bg-spotify-darkGray text-white hover:bg-spotify-darkerGray'
                }`}
            >
              All
            </button>
            {MOOD_OPTIONS.map((mood) => (
              <button
                key={mood.value}
                onClick={() => handleMoodChange(mood.value)}
                className={`px-5 py-2 rounded-full font-semibold transition-all ${selectedMood === mood.value
                    ? 'bg-spotify-green text-black'
                    : 'bg-spotify-darkGray text-white hover:bg-spotify-darkerGray'
                  }`}
                title={mood.description}
              >
                {mood.label}
              </button>
            ))}
          </div>
        </div>

        {explanation && (
          <div className="bg-spotify-darkerGray rounded-lg p-4 border-l-4 border-spotify-green">
            <p className="text-spotify-lightGray text-sm">{explanation}</p>
          </div>
        )}

        {loadingRecommendations ? (
          <div className="flex items-center justify-center py-12">
            <div className="text-spotify-lightGray">
              Finding the perfect tracks for you...
            </div>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-white">
                {recommendations.length > 0
                  ? `Recommended Tracks (${recommendations.length})`
                  : 'No recommendations found'}
              </h2>
              {recommendations.length > 0 && (
                <button
                  onClick={() => setShowPlaylistModal(true)}
                  className="bg-spotify-green text-black font-semibold px-5 py-2 rounded-full hover:scale-105 transition-transform flex items-center space-x-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  <span>Create Playlist</span>
                </button>
              )}
            </div>

            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
              {recommendations.map((track) => (
                <TrackCard
                  key={track.id}
                  track={track}
                  onPlay={handlePlayTrack}
                />
              ))}
            </div>
          </>
        )}
      </div>

      <PlaylistModal
        isOpen={showPlaylistModal}
        onClose={() => setShowPlaylistModal(false)}
        tracks={recommendations}
        onCreatePlaylist={handleCreatePlaylist}
      />
    </Layout>
  );
}
