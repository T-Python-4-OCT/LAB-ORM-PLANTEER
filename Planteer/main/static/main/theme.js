// Persist the color scheme in a first-party cookie and apply it before interaction.
(() => {
  const root = document.documentElement;
  const toggle = document.querySelector(".theme-toggle");
  const menuToggle = document.querySelector(".menu-toggle");
  const navLinks = document.querySelector(".nav-links");
  const themeCookie = document.cookie
    .split("; ")
    .find((cookie) => cookie.startsWith("planteer_theme="));

  if (themeCookie) {
    const savedTheme = themeCookie.split("=")[1];
    if (savedTheme === "light" || savedTheme === "dark") {
      root.dataset.theme = savedTheme;
    }
  }

  const updateThemeControl = () => {
    if (!toggle) return;
    const isDark = root.dataset.theme === "dark";
    toggle.querySelector(".theme-icon").textContent = isDark ? "☀" : "☾";
    toggle.querySelector(".theme-label").textContent = isDark
      ? "Light mode"
      : "Dark mode";
  };

  updateThemeControl();
  toggle?.addEventListener("click", () => {
    const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
    root.dataset.theme = nextTheme;
    document.cookie = `planteer_theme=${nextTheme}; Max-Age=31536000; Path=/; SameSite=Lax`;
    updateThemeControl();
  });

  // Keep the mobile navigation accessible to keyboard and touch users.
  menuToggle?.addEventListener("click", () => {
    const isExpanded = menuToggle.getAttribute("aria-expanded") === "true";
    menuToggle.setAttribute("aria-expanded", String(!isExpanded));
    navLinks?.classList.toggle("nav-open", !isExpanded);
  });
})();
