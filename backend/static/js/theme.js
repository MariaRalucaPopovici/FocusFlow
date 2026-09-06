document.addEventListener("DOMContentLoaded", function () {
    const themeSelect = document.getElementById("theme-select");
    // Retrieve the previously selected theme
    const savedTheme =
        localStorage.getItem("focusflow-theme") || "notepad";
    // Apply it to the whole page
    document.documentElement.dataset.theme = savedTheme;
    // If the selector exists on this page
    if (themeSelect) {
        // Make dropdown display saved choice
        themeSelect.value = savedTheme;
        // Change theme immediately when user selects one
        themeSelect.addEventListener("change", function () {
            const selectedTheme = themeSelect.value;
            document.documentElement.dataset.theme = selectedTheme;
            localStorage.setItem(
                "focusflow-theme",
                selectedTheme
            );
        });
    }
});