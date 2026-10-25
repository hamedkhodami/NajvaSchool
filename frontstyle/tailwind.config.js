/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../src/templates/**/*.{html,htm,txt,jinja}",
    "../src/apps/**/*.{html,htm,txt,jinja}",
    "../src/static/**/*.{js,html}",
    "../src/apps/**/static/**/*.{js,html}",
  ],

  safelist: [
    // اندازه‌ها
    "px-4", "px-5",
    "py-2", "py-2.5", "py-3",

    // رنگ‌ها
    "bg-primary",
    "hover:bg-primary-hover",
    "focus:ring-primary",
    "text-white",

    // دکمه‌ها
    "rounded-xl",
    "rounded-2xl",
    "inline-flex",
    "items-center",
    "justify-center",
    "font-bold",
    "shadow-card",
    "shadow-lift",

    // نمایش
    "md:block",
    "md:hidden",
    "sm:block",
    "sm:hidden",

    // قبلی‌ها
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
    "sm:grid-cols-2",
    "md:grid-cols-3",
    "lg:grid-cols-4",
    "lg:grid-cols-3",
    "lg:grid-cols-2",
    "sm:block",
    "sm:hidden",
  ],

  theme: {
    container: {
      center: true,
      padding: "1rem",
    },

    extend: {
      colors: {
        brand: {
          DEFAULT: "#101F33",
          hover: "#17293F",
          active: "#0B1524",
          soft: "#E8EDF3",
        },

        accent: {
          DEFAULT: "#9A6B1F",
          hover: "#7A5115",
          soft: "#F7EDD6",
          light: "#D0A241",
        },

        surface: {
          page: "#F1F5F9",
          public: "#FAF8F3",
          card: "#FFFFFF",
          muted: "#F8FAFC",
          border: "#E2E8F0",
        },

        dashboard: {
          bg: "#F1F5F9",
        },

        public: {
          bg: "#FAF8F3",
        },

        ink: {
          900: "#0B1524",
          800: "#101F33",
          700: "#17293F",
          600: "#33465D",
          400: "#64748B",
          300: "#94A3B8",
        },

        brass: {
          700: "#7A5115",
          600: "#9A6B1F",
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

        success: {
          DEFAULT: "#1F7A5C",
          soft: "#E7F4ED",
        },

        warning: {
          DEFAULT: "#A16207",
          soft: "#FEF3C7",
        },

        danger: {
          DEFAULT: "#C2413B",
          soft: "#FDECEC",
        },

        info: {
          DEFAULT: "#2563A6",
          soft: "#EAF2FC",
        },
      },

      fontFamily: {
        sans: ["Yekan", "Vazirmatn", "system-ui", "sans-serif"],
      },

      boxShadow: {
        card: "0 2px 8px rgba(11,21,36,.04), 0 12px 32px -24px rgba(11,21,36,.24)",
        lift: "0 8px 24px -12px rgba(11,21,36,.18), 0 2px 6px rgba(11,21,36,.04)",
        header: "0 4px 24px rgba(11,21,36,.045)",
      },

      maxWidth: {
        screen: "1200px",
      },

      backgroundImage: {
        "gold-gradient": "linear-gradient(135deg, #D0A241, #9A6B1F)",
        "hero-gradient": "linear-gradient(135deg, #FAF8F3 0%, #F2EBDD 55%, #FFFFFF 100%)",
        "navy-gradient": "linear-gradient(135deg, #101F33 0%, #203956 100%)",
      },

      transitionDuration: {
        400: "400ms",
      },
    },
  },

  plugins: [],
};
