import type { MoodOption, TimeRangeOption } from '../types/spotify';

export const API_BASE_URL = 'http://127.0.0.1:8000';
export const FRONTEND_PORT = 3000;

export const MOOD_OPTIONS: MoodOption[] = [
  { value: 'happy', label: 'Happy', description: 'Upbeat and positive vibes' },
  { value: 'chill', label: 'Chill', description: 'Relaxed and mellow atmosphere' },
  { value: 'workout', label: 'Workout', description: 'High-energy beats' },
  { value: 'sad', label: 'Sad', description: 'Emotional and introspective tones' },
  { value: 'energetic', label: 'Energetic', description: 'Dynamic and powerful rhythms' }
];

export const TIME_RANGE_OPTIONS: TimeRangeOption[] = [
  { value: 'short_term', label: 'Last 4 Weeks' },
  { value: 'medium_term', label: 'Last 6 Months' },
  { value: 'long_term', label: 'All Time' }
];
