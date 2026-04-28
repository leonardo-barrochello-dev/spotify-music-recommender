import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../../components/Layout/Layout';
import TrackCard from '../../components/TrackCard/TrackCard';
import { useAuth } from '../../hooks/useAuth';
import { userService } from '../../services/musicService';
import { TIME_RANGE_OPTIONS } from '../../utils/constants';
import type { SpotifyUser, SpotifyTrack, SpotifyArtist } from '../../types/spotify';

export default function Dashboard() {
  const { isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();
  const [topTracks, setTopTracks] = useState<SpotifyTrack[]>([]);
  const [topArtists, setTopArtists] = useState<SpotifyArtist[]>([]);
  const [user, setUser] = useState<SpotifyUser | null>(null);
  const [timeRange, setTimeRange] = useState('medium_term');
  const [loadingData, setLoadingData] = useState(true);

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, loading, navigate]);

  useEffect(() => {
    if (isAuthenticated) {
      loadProfile();
    }
  }, [isAuthenticated, timeRange]);

  const loadProfile = async () => {
    setLoadingData(true);
    try {
      const [profileData, tracks, artists] = await Promise.all([
        userService.getProfile(),
        userService.getTopTracks(20, timeRange),
        userService.getTopArtists(10, timeRange),
      ]);
      setUser(profileData);
      setTopTracks(tracks);
      setTopArtists(artists);
    } catch (error) {
      console.error('Failed to load profile:', error);
    } finally {
      setLoadingData(false);
    }
  };

  const handlePlayTrack = (track: SpotifyTrack) => {
    window.open(track.external_urls?.spotify, '_blank');
  };

  if (loading || loadingData) {
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
      <div className="space-y-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">
              Welcome back, {user?.display_name}!
            </h1>
            <p className="text-spotify-lightGray">
              Here's what you've been listening to lately
            </p>
          </div>

          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="bg-spotify-darkGray text-white px-4 py-2 rounded-full focus:outline-none focus:ring-2 focus:ring-spotify-green"
          >
            {TIME_RANGE_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <section>
          <h2 className="text-2xl font-bold text-white mb-4">Top Artists</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {topArtists.map((artist) => {
              const image = artist.images?.[0]?.url || 'https://via.placeholder.com/200x200?text=Artist';
              return (
                <div
                  key={artist.id}
                  className="bg-spotify-darkerGray rounded-lg p-4 hover:bg-spotify-darkGray transition-all cursor-pointer group"
                  onClick={() => window.open(artist.external_urls?.spotify, '_blank')}
                >
                  <img
                    src={image}
                    alt={artist.name}
                    className="w-full aspect-square object-cover rounded-full mb-3 shadow-lg"
                  />
                  <h3 className="text-white font-semibold truncate" title={artist.name}>
                    {artist.name}
                  </h3>
                </div>
              );
            })}
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-white mb-4">Top Tracks</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
            {topTracks.map((track) => (
              <TrackCard
                key={track.id}
                track={track}
                onPlay={handlePlayTrack}
              />
            ))}
          </div>
        </section>

        <section className="bg-gradient-to-r from-spotify-green to-emerald-600 rounded-lg p-6">
          <h2 className="text-2xl font-bold text-black mb-2">
            Ready for new discoveries?
          </h2>
          <p className="text-black mb-4">
            Get personalized recommendations based on your listening habits
          </p>
          <button
            onClick={() => navigate('/recommendations')}
            className="bg-black text-white font-semibold px-6 py-3 rounded-full hover:scale-105 transition-transform"
          >
            Get Recommendations
          </button>
        </section>
      </div>
    </Layout>
  );
}
