/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../src/templates/**/*.{html,htm,txt,jinja}",
    "../src/static/**/*.{js,html}",
    "./*.html",
    "./*.js"
  ],

  safelist: [
    "text-[13.5px]",
    "text-[14px]",
    "text-[14.5px]",
    "text-[15px]",
    "text-[15.5px]",
    "text-[16px]",
    "text-[18px]",
    "text-[22px]",
    "text-[24px]",
    "text-[30px]",
    "leading-[1.35]",
    "leading-[1.3]",
    "tracking-tight",
    "aspect-[16/9]",
    "aspect-[4/3]",

    "lg:grid-cols-[1.3fr_1fr]",
    "lg:grid-cols-[minmax(0,1fr)_minmax(0,1.05fr)]",

    "shadow-card",
    "shadow-lift",

    "rounded-2xl",
    "rounded-xl",

    "sm:grid-cols-2",
    "md:grid-cols-3",
    "lg:grid-cols-4",
    "lg:grid-cols-3",
    "lg:grid-cols-2",
    "sm:block",
    "sm:hidden"
  ],

  theme: {
    container: { center: true, padding: "1rem" },

    extend: {
      colors: {
        primary: "#00095C",

        auth: {
          navy: "#00095C",
        },

        dashboard: {
          bg: "#F1F5F9",
        },

        public: {
          bg: "#FAF9F6",

        },

        ink: {
          900: "#0B1524",
          800: "#101F33",
          700: "#17293F",
          600: "#22364F",
          400: "#5A6B80",
          300: "#8494A6",
        },

        brass: {
          700: "#7A5B18",
          600: "#9A7423",
          500: "#B98A2E",
          400: "#D0A241",
          300: "#E1BE69",
          200: "#EDD9A6",
          100: "#F7EDD6",
        },

        paper: {
          DEFAULT: "#F5F4F1",
          card: "#FFFFFF",
          line: "#E4E2DC",
        },

        up: "#1F7A5C",
        down: "#C2413B",
      },

      fontFamily: {
        sans: ["Yekan", "Vazirmatn", "system-ui", "sans-serif"],
      },

      boxShadow: {
        card: "0 1px 1px rgba(11,21,36,.04), 0 10px 30px -22px rgba(11,21,36,.5)",
        lift: "0 2px 4px rgba(11,21,36,.05), 0 18px 40px -24px rgba(11,21,36,.55)",
      },

      maxWidth: {
        screen: "1200px",
      },

      backgroundImage: {
        "gold-gradient": "linear-gradient(to right, #D4AF37, #B8860B)",
      },
    },
  },

  plugins: [],
};
