(() => {
    const themeStorageKey = "planteer-theme";
    const leafMaskReach = 0.3;
    const root = document.documentElement;
    const themeButton = document.querySelector("[data-theme-toggle]");
    const favicon = document.querySelector('link[rel="icon"][type="image/svg+xml"]');
    const themeColor = document.querySelector('meta[name="theme-color"]');
    const systemPrefersNight = matchMedia("(prefers-color-scheme: dark)");
    const prefersReducedMotion = matchMedia("(prefers-reduced-motion: reduce)");

    function getSavedTheme() {
        try {
            return localStorage.getItem(themeStorageKey);
        } catch {
            return null;
        }
    }

    function applyTheme(theme) {
        root.dataset.theme = theme;
        themeButton?.setAttribute("aria-pressed", String(theme === "night"));

        if (favicon) {
            favicon.href = favicon.dataset[theme];
        }
        if (themeColor) {
            const backgroundColor = getComputedStyle(root).getPropertyValue("--paper");
            themeColor.content = backgroundColor.trim();
        }
    }

    async function switchTheme(theme) {
        if (!document.startViewTransition) {
            applyTheme(theme);
            return;
        }
        if (prefersReducedMotion.matches) {
            document.startViewTransition(() => applyTheme(theme));
            return;
        }

        const { left, top, width, height } = themeButton.getBoundingClientRect();
        const centerX = left + width / 2;
        const centerY = top + height / 2;
        const farthestX = Math.max(centerX, innerWidth - centerX);
        const farthestY = Math.max(centerY, innerHeight - centerY);
        const maskSize = Math.hypot(farthestX, farthestY) / leafMaskReach;

        root.classList.add("theme-shift");
        const transition = document.startViewTransition(() => applyTheme(theme));
        const clearTransitionClass = () => root.classList.remove("theme-shift");
        transition.finished.then(clearTransitionClass, clearTransitionClass);

        try {
            await transition.ready;
        } catch {
            return;
        }

        root.animate(
            {
                maskSize: ["0px 0px", `${maskSize}px ${maskSize}px`],
                maskPosition: [
                    `${centerX}px ${centerY}px`,
                    `${centerX - maskSize / 2}px ${centerY - maskSize / 2}px`,
                ],
            },
            {
                duration: 1000,
                easing: "cubic-bezier(.6, 0, .2, 1)",
                pseudoElement: "::view-transition-new(root)",
            },
        );
    }

    applyTheme(root.dataset.theme === "night" ? "night" : "day");

    themeButton?.addEventListener("click", () => {
        const nextTheme = root.dataset.theme === "night" ? "day" : "night";
        try {
            localStorage.setItem(themeStorageKey, nextTheme);
        } catch {}
        switchTheme(nextTheme);
    });

    systemPrefersNight.addEventListener("change", (event) => {
        if (!getSavedTheme()) {
            applyTheme(event.matches ? "night" : "day");
        }
    });
})();
