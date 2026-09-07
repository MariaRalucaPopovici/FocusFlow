document.addEventListener("DOMContentLoaded", function () {
    const THEME_ICONS = {
        notepad: "📓",
        autumn: "🍂",
        winter: "❄️",
        christmas: "🎄",
        spring: "🌸",
        easter: "🐣",
        summer: "☀️",
        midnight: "🌙",
        "autumn-dark": "🍁",
    };
    const THEME_ORDER = Object.keys(THEME_ICONS);

    const savedTheme = localStorage.getItem("focusflow-theme") || "notepad";
    document.documentElement.dataset.theme = savedTheme;

    const themeToggle = document.getElementById("theme-toggle");
    if (themeToggle) {
        themeToggle.textContent = THEME_ICONS[savedTheme] || "📓";
        themeToggle.title = "Theme: " + savedTheme + " (click to change)";

        themeToggle.addEventListener("click", function () {
            const currentTheme = document.documentElement.dataset.theme;
            const currentIndex = THEME_ORDER.indexOf(currentTheme);
            const nextTheme = THEME_ORDER[(currentIndex + 1) % THEME_ORDER.length];

            document.documentElement.dataset.theme = nextTheme;
            localStorage.setItem("focusflow-theme", nextTheme);
            themeToggle.textContent = THEME_ICONS[nextTheme];
            themeToggle.title = "Theme: " + nextTheme + " (click to change)";
        });
    }
});