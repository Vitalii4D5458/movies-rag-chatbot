// tailwind.config.js
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      animation: {
        bounce: "bounce 1s infinite",
      },
      keyframes: {
        bounce: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-0.5px)" },
        },
      },
      animationDelay: {
        200: "0.2s",
        400: "0.4s",
      },
    },
  },
  plugins: [],
};
