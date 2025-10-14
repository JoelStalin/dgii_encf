import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx,jsx,js}"],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#2563eb",
          foreground: "#ffffff",
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
