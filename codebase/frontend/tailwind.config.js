/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"]
      },
      boxShadow: {
        glow: "0 0 45px rgba(124,58,237,.20)",
        cyan: "0 0 35px rgba(34,211,238,.12)"
      }
    }
  },
  plugins: []
};
