(function () {

    let currentTheme = localStorage.getItem("planteer-theme");

    if (currentTheme !== "dark" && currentTheme !== "light") {
        currentTheme = "light";
    }

    document.documentElement.setAttribute(
        "data-bs-theme",
        currentTheme
    );

    document.addEventListener("DOMContentLoaded", function () {

        const themeToggle = document.getElementById("themeToggle");

        if (!themeToggle) return;

        function updateIcon() {

            const isDark = currentTheme === "dark";

            themeToggle.innerHTML = isDark
                ? '<i class="bi bi-sun"></i>'
                : '<i class="bi bi-moon"></i>';

            themeToggle.setAttribute(
                "aria-label",
                isDark ? "Enable light mode" : "Enable dark mode"
            );

        }

        updateIcon();

        themeToggle.addEventListener("click", function () {

            currentTheme = currentTheme === "dark"
                ? "light"
                : "dark";

            document.documentElement.setAttribute(
                "data-bs-theme",
                currentTheme
            );

            localStorage.setItem(
                "planteer-theme",
                currentTheme
            );

            updateIcon();

        });

    });

})();