/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#09090B',
        primary: '#FFFFFF',
        accent: {
          DEFAULT: '#3B82F6',
          hover: '#2563EB',
        },
        'accent-secondary': '#8B5CF6',
        success: '#10B981',
        surface: '#18181B',
        'surface-hover': '#27272A',
        border: '#27272A',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
