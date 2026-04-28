import { useState, FormEvent } from 'react';
import type { SpotifyTrack } from '../../types/spotify';

interface PlaylistModalProps {
  isOpen: boolean;
  onClose: () => void;
  tracks: SpotifyTrack[];
  onCreatePlaylist: (name: string, description: string, trackUris: string[]) => Promise<void>;
}

export default function PlaylistModal({ isOpen, onClose, tracks, onCreatePlaylist }: PlaylistModalProps) {
  const [playlistName, setPlaylistName] = useState('My Recommended Mix');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const trackUris = tracks.map((t) => `spotify:track:${t.id}`);
      await onCreatePlaylist(playlistName, description, trackUris);
      onClose();
      setPlaylistName('My Recommended Mix');
      setDescription('');
    } catch (error) {
      console.error('Failed to create playlist:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
      <div className="bg-spotify-darkGray rounded-lg p-6 w-full max-w-md">
        <h2 className="text-2xl font-bold text-white mb-4">Create Playlist</h2>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-spotify-lightGray text-sm mb-2">
              Playlist Name
            </label>
            <input
              type="text"
              value={playlistName}
              onChange={(e) => setPlaylistName(e.target.value)}
              className="w-full bg-spotify-darkerGray text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-spotify-green"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-spotify-lightGray text-sm mb-2">
              Description (optional)
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-spotify-darkerGray text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-spotify-green resize-none"
              rows={3}
            />
          </div>

          <div className="mb-4">
            <p className="text-spotify-lightGray text-sm">
              {tracks.length} tracks will be added
            </p>
          </div>

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-spotify-lightGray hover:text-white transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-spotify-green text-black font-semibold rounded-full hover:scale-105 transition-transform disabled:opacity-50"
            >
              {loading ? 'Creating...' : 'Create Playlist'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
