import { useAuth } from '../../hooks/useAuth';
import type { SpotifyUser } from '../../types/spotify';

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="h-16 bg-spotify-darkerGray flex items-center justify-between px-6">
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <svg
            className="w-8 h-8 text-spotify-green"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.6 0 12 0zm5.5 17.3c-.2.3-.5.4-.8.2-2.1-1.3-4.8-1.6-8-.9-2.4.5-4.4.1-5.3-.1-.3-.1-.5-.4-.4-.7.1-.3.4-.5.7-.4 1.3.3 3.8.8 7.2.2 3.5-.6 6.5-.2 8.9 1.2.3.2.4.5.2.8zm1.1-2.6c-.3.4-.8.5-1.2.3-2.5-1.5-6.3-2-9.3-1.1-2.5.7-5.1.3-6.4-.1-.5-.1-.7-.6-.6-1.1.1-.5.6-.7 1.1-.6 1.9.6 5.1 1 8.5 0 3.5-1 7.8-.4 10.8 1.4.4.2.6.8.4 1.2zm.1-2.7c-2.8-1.7-7.5-2.3-10.9-1.3-2.9.8-6.3.4-7.9-.1-.6-.2-.9-.8-.7-1.4.2-.6.8-.9 1.4-.7 2.1.7 6 1.1 9.5.1 3.9-1.1 9.1-.4 12.4 1.6.6.4.8 1.1.4 1.7-.3.5-1 .7-1.6.4z" />
          </svg>
          <span className="text-white font-semibold">Spotify</span>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        {user && (
          <>
            <div className="flex items-center space-x-2">
              {user.images?.[0]?.url ? (
                <img
                  src={user.images[0].url}
                  alt={user.display_name}
                  className="w-8 h-8 rounded-full"
                />
              ) : (
                <div className="w-8 h-8 rounded-full bg-spotify-green flex items-center justify-center text-spotify-black font-bold">
                  {user.display_name?.[0]?.toUpperCase() || 'U'}
                </div>
              )}
              <span className="text-white text-sm">{user.display_name}</span>
            </div>
            <button
              onClick={logout}
              className="text-spotify-lightGray hover:text-white text-sm transition-colors"
            >
              Logout
            </button>
          </>
        )}
      </div>
    </header>
  );
}
