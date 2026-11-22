const footerBottom = document.querySelector(".footer-bottom");

function updateBackToTop() {
  const pageHeight = document.documentElement.scrollHeight - footerBottom.offsetHeight;
  footerBottom.hidden = pageHeight < window.innerHeight * 2;
}

new ResizeObserver(updateBackToTop).observe(document.body);
window.addEventListener("resize", updateBackToTop);
updateBackToTop();
