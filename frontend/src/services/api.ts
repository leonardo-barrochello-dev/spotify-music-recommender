import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const sessionToken = localStorage.getItem('session_token');
  if (sessionToken) {
    config.params = {
      ...config.params,
      session_token: sessionToken,
    };
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const detail = error.response?.data?.detail;
      
      // Sessão expirou no backend (restart ou timeout)
      if (detail === "SESSION_EXPIRED" || detail === "Spotify token not found") {
        console.log('[API] Session expired, clearing localStorage');
        localStorage.removeItem('session_token');
        
        // Se não estiver na página de login, redirect
        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

export default api;
