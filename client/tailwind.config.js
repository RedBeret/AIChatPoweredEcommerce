// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
    purge: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {
            colors: {
                coolGray: "#DFE5EA",
                phoneBg: "#06070C",
            },
            gridTemplateRows: {
                "[auto,auto,1fr]": "auto auto 1fr",
            },
            textShadow: {
                default: "2px 2px 4px rgba(0, 0, 0, 0.5)",
            },
        },
    },
    variants: {
        extend: {},
    },
    plugins: [
        require("@tailwindcss/aspect-ratio"),
        require("@tailwindcss/forms"),
        require("@tailwindcss/typography"),
    ],
};
