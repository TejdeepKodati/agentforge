/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        darkBg: "#0B0F19",
        cardBg: "#111827",
        borderSubtle: "#1F2937",
        brandPrimary: "#3B82F6",
        brandSecondary: "#8B5CF6",
      },
    },
  },
  plugins: [],
};
