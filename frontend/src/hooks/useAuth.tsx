import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import api from '../services/api';
import type { SpotifyUser } from '../types/spotify';

interface AuthContextType {
  user: SpotifyUser | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: () => void;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<SpotifyUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const sessionToken = localStorage.getItem('session_token');
    console.log('[Auth] Session token on mount:', sessionToken ? 'EXISTS' : 'NOT FOUND');
    
    if (sessionToken) {
      loadUser(sessionToken);
    } else {
      setLoading(false);
    }
  }, []);

  const loadUser = async (token: string) => {
    console.log('[Auth] Loading user with token...');
    try {
      const response = await api.get<SpotifyUser>('/user/profile', {
        params: { session_token: token }
      });
      console.log('[Auth] User loaded:', response.data.display_name);
      setUser(response.data);
    } catch (error: any) {
      console.error('[Auth] Failed to load user:', error.response?.status, error.message);
      
      // Token inválido - limpa localStorage
      if (error.response?.status === 401) {
        localStorage.removeItem('session_token');
        console.log('[Auth] Token invalid, cleared localStorage');
      }
      
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = () => {
    console.log('[Auth] Login called, redirecting to:', `${api.defaults.baseURL}/auth/login`);
    window.location.href = `${api.defaults.baseURL}/auth/login`;
  };

  const logout = async () => {
    console.log('[Auth] Logout called');
    
    // 1. Limpa localStorage IMEDIATAMENTE (antes de qualquer async)
    localStorage.removeItem('session_token');
    console.log('[Auth] Token removed from localStorage');
    
    // 2. Limpa estado React
    setUser(null);
    
    // 3. Chama backend para invalidar sessão (fire-and-forget)
    try {
      await api.get('/auth/logout');
    } catch (error) {
      console.error('Logout backend error:', error);
    }
    
    // 4. Força reload completo da página
    window.location.href = '/login';
  };

  const value: AuthContextType = {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    logout,
  };

  console.log('[Auth] Context value:', { isAuthenticated: value.isAuthenticated, loading: value.loading });
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
