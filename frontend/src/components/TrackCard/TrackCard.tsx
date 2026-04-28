import type { SpotifyTrack } from '../../types/spotify';

interface TrackCardProps {
  track: SpotifyTrack;
  onPlay?: (track: SpotifyTrack) => void;
  onAdd?: (track: SpotifyTrack) => void;
}

export default function TrackCard({ track, onPlay, onAdd }: TrackCardProps) {
  const albumImage = track.album?.images?.[0]?.url || 'https://via.placeholder.com/300x300?text=No+Cover';
  const artistNames = track.artists?.map((a) => a.name).join(', ') || 'Unknown Artist';

  return (
    <div className="bg-spotify-darkerGray rounded-lg p-4 hover:bg-spotify-darkGray transition-all group cursor-pointer">
      <div className="relative mb-4">
        <img
          src={albumImage}
          alt={track.album?.name || 'Album cover'}
          className="w-full aspect-square object-cover rounded-md shadow-lg"
        />
        <button
          onClick={() => onPlay?.(track)}
          className="absolute bottom-2 right-2 w-12 h-12 bg-spotify-green rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity shadow-xl hover:scale-105"
        >
          <svg className="w-6 h-6 text-black ml-1" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z" />
          </svg>
        </button>
      </div>

      <h3 className="text-white font-semibold truncate mb-1" title={track.name}>
        {track.name}
      </h3>
      <p className="text-spotify-lightGray text-sm truncate mb-3" title={artistNames}>
        {artistNames}
      </p>

      <div className="flex items-center justify-between">
        <span className="text-xs text-spotify-lightGray">
          {Math.floor(track.duration_ms / 60000)}:
          {String((track.duration_ms % 60000) / 1000).padStart(2, '0')}
        </span>
        {onAdd && (
          <button
            onClick={() => onAdd(track)}
            className="text-spotify-lightGray hover:text-spotify-green transition-colors"
            title="Add to playlist"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}
