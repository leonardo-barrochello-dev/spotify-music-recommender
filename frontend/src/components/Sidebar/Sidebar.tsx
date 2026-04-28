import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

export default function Sidebar() {
  const location = useLocation();
  const { isAuthenticated } = useAuth();

  const navItems = [
    { path: '/dashboard', label: 'Home' },
    { path: '/recommendations', label: 'Recommendations' },
  ];

  return (
    <aside className="w-64 bg-spotify-black h-full flex flex-col">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-white">Music Recommender</h1>
      </div>

      <nav className="flex-1 px-4">
        <ul className="space-y-2">
          {navItems.map((item) => (
            <li key={item.path}>
              <Link
                to={item.path}
                className={`block px-4 py-3 rounded-lg transition-colors ${
                  location.pathname === item.path
                    ? 'bg-spotify-darkGray text-white'
                    : 'text-spotify-lightGray hover:text-white hover:bg-spotify-darkGray'
                }`}
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      <div className="p-4 border-t border-spotify-darkGray">
        <p className="text-xs text-spotify-lightGray">
          Powered by Spotify API & TensorFlow
        </p>
      </div>
    </aside>
  );
}
