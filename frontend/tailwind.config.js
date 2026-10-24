/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        finance: {
          navy: "#0A192F",
          dark: "#020C1B",
          slate: "#1E293B",
          accent: "#2563EB",
          danger: "#DC2626",
          warning: "#D97706",
          success: "#059669",
        }
      }
    },
  },
  plugins: [],
}
