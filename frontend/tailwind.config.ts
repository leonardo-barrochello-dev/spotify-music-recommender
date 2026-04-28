import type { Config } from 'tailwindcss';

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        spotify: {
          green: '#1DB954',
          black: '#191414',
          darkGray: '#282828',
          lightGray: '#B3B3B3',
          white: '#FFFFFF',
          darkerGray: '#181818',
          cardGray: '#121212'
        }
      },
      fontFamily: {
        sans: ['Circular', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [],
} satisfies Config;
