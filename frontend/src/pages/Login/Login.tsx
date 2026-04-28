import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

export default function Login() {
  const { isAuthenticated, loading, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const storedToken = localStorage.getItem('session_token');
    console.log('[Login] Page loaded', {
      hasTokenInLocalStorage: storedToken !== null,
      tokenLength: storedToken?.length || 0
    });

    console.log('[Login] useEffect triggered', {
      isAuthenticated,
      loading,
      hasTokenInUrl: new URLSearchParams(location.search).get('session_token') !== null
    });

    // Verifica se há session_token na URL (vindo do callback do Spotify)
    const params = new URLSearchParams(location.search);
    const urlToken = params.get('session_token');

    if (urlToken) {
      console.log('[Login] Found session_token in URL, saving...');
      localStorage.setItem('session_token', urlToken);
      // Limpa a URL e recarrega para garantir que o AuthProvider detecte o token
      window.location.href = '/dashboard';
      return;
    }

    // Se já está autenticado, podemos mostrar uma mensagem ou manter na página para permitir re-login
    if (!loading && isAuthenticated) {
      console.log('[Login] User is already authenticated, staying on page to allow re-login if desired');
    }
  }, [isAuthenticated, loading, navigate, location.search]);

  const handleLogin = () => {
    console.log('[Login] Login button clicked');
    login();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-spotify-black via-spotify-darkGray to-spotify-cardGray flex items-center justify-center p-4">
      <div className="max-w-md w-full text-center">
        <div className="mb-8">
          <svg
            className="w-24 h-24 mx-auto text-spotify-green mb-6"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.6 0 12 0zm5.5 17.3c-.2.3-.5.4-.8.2-2.1-1.3-4.8-1.6-8-.9-2.4.5-4.4.1-5.3-.1-.3-.1-.5-.4-.4-.7.1-.3.4-.5.7-.4 1.3.3 3.8.8 7.2.2 3.5-.6 6.5-.2 8.9 1.2.3.2.4.5.2.8zm1.1-2.6c-.3.4-.8.5-1.2.3-2.5-1.5-6.3-2-9.3-1.1-2.5.7-5.1.3-6.4-.1-.5-.1-.7-.6-.6-1.1.1-.5.6-.7 1.1-.6 1.9.6 5.1 1 8.5 0 3.5-1 7.8-.4 10.8 1.4.4.2.6.8.4 1.2zm.1-2.7c-2.8-1.7-7.5-2.3-10.9-1.3-2.9.8-6.3.4-7.9-.1-.6-.2-.9-.8-.7-1.4.2-.6.8-.9 1.4-.7 2.1.7 6 1.1 9.5.1 3.9-1.1 9.1-.4 12.4 1.6.6.4.8 1.1.4 1.7-.3.5-1 .7-1.6.4z" />
          </svg>
          <h1 className="text-4xl font-bold text-white mb-2">
            Music Recommender
          </h1>
          <p className="text-spotify-lightGray text-lg">
            Discover your next favorite song with AI-powered recommendations
          </p>
        </div>

        <div className="bg-spotify-darkerGray rounded-lg p-8 mb-6">
          <h2 className="text-xl font-semibold text-white mb-4">
            How it works
          </h2>
          <ul className="text-left text-spotify-lightGray space-y-3">
            <li className="flex items-start">
              <span className="text-spotify-green mr-3">✓</span>
              <span>Analyze your top tracks and artists</span>
            </li>
            <li className="flex items-start">
              <span className="text-spotify-green mr-3">✓</span>
              <span>Use TensorFlow to find similar music</span>
            </li>
            <li className="flex items-start">
              <span className="text-spotify-green mr-3">✓</span>
              <span>Get personalized recommendations</span>
            </li>
            <li className="flex items-start">
              <span className="text-spotify-green mr-3">✓</span>
              <span>Create playlists directly on Spotify</span>
            </li>
          </ul>
        </div>

        <button
          onClick={handleLogin}
          className="w-full bg-spotify-green text-black font-bold py-4 px-8 rounded-full hover:scale-105 transition-transform flex items-center justify-center space-x-3"
        >
          <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.6 0 12 0zm5.5 17.3c-.2.3-.5.4-.8.2-2.1-1.3-4.8-1.6-8-.9-2.4.5-4.4.1-5.3-.1-.3-.1-.5-.4-.4-.7.1-.3.4-.5.7-.4 1.3.3 3.8.8 7.2.2 3.5-.6 6.5-.2 8.9 1.2.3.2.4.5.2.8zm1.1-2.6c-.3.4-.8.5-1.2.3-2.5-1.5-6.3-2-9.3-1.1-2.5.7-5.1.3-6.4-.1-.5-.1-.7-.6-.6-1.1.1-.5.6-.7 1.1-.6 1.9.6 5.1 1 8.5 0 3.5-1 7.8-.4 10.8 1.4.4.2.6.8.4 1.2zm.1-2.7c-2.8-1.7-7.5-2.3-10.9-1.3-2.9.8-6.3.4-7.9-.1-.6-.2-.9-.8-.7-1.4.2-.6.8-.9 1.4-.7 2.1.7 6 1.1 9.5.1 3.9-1.1 9.1-.4 12.4 1.6.6.4.8 1.1.4 1.7-.3.5-1 .7-1.6.4z" />
          </svg>
          <span>Login with Spotify</span>
        </button>
      </div>
    </div>
  );
}
