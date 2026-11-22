const toggle = document.querySelector(".theme-button");
const root = document.documentElement;

const syncThemeButton = () => {
  toggle.setAttribute("aria-pressed", String(root.dataset.theme === "dark"));
};

toggle.hidden = false;
syncThemeButton();
toggle.addEventListener("click", () => {
  const theme = root.dataset.theme === "dark" ? "light" : "dark";
  root.dataset.theme = theme;
  document.cookie = "planteer_theme=" + theme + "; Path=/; Max-Age=31536000; SameSite=Lax" +
    (location.protocol === "https:" ? "; Secure" : "");
  syncThemeButton();
});
