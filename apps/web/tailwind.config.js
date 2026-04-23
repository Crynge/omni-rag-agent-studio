/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#091017",
        bronze: "#dca567",
        mint: "#71e1bf",
        ember: "#ff7d62"
      },
      fontFamily: {
        display: ["Georgia", "serif"],
        body: ["ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["ui-monospace", "SFMono-Regular", "monospace"]
      },
      boxShadow: {
        panel: "0 26px 80px rgba(0, 0, 0, 0.32)"
      }
    },
  },
  plugins: [],
};

