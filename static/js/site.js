document.querySelectorAll('.ticker').forEach(ticker => {
  const group = ticker.firstElementChild;
  if (!group || ticker.querySelector('.ticker-track')) return;
  group.classList.add('ticker-group');
  const duplicate = group.cloneNode(true);
  duplicate.setAttribute('aria-hidden', 'true');
  const track = document.createElement('div');
  track.className = 'ticker-track';
  track.append(group, duplicate);
  ticker.append(track);
});

document.querySelectorAll('img').forEach(image => {
  image.addEventListener('error', () => {
    if (!image.dataset.fallback) {
      image.dataset.fallback = 'true';
      image.src = '/static/images/plant-placeholder.svg';
    }
  });
});

// Keep content visible without JavaScript or when reduced motion is preferred.
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
if (!reducedMotion.matches && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.section-heading, .plant-card, .category-grid > a, .story, .closing, .message-card').forEach(element => {
    const siblings = Array.from(element.parentElement.children);
    element.style.setProperty('--reveal-delay', `${(siblings.indexOf(element) % 4) * 65}ms`);
    element.classList.add('reveal');
    observer.observe(element);
  });
  reducedMotion.addEventListener('change', event => {
    if (event.matches) {
      observer.disconnect();
      document.querySelectorAll('.reveal').forEach(element => element.classList.add('is-visible'));
    }
  });
}

const backToTop = document.createElement('button');
backToTop.className = 'back-to-top';
backToTop.type = 'button';
backToTop.setAttribute('aria-label', 'Back to top');
backToTop.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 14 6-6 6 6"/></svg>';
backToTop.hidden = true;
document.body.append(backToTop);
let scrollScheduled = false;
const updateScroll = () => {
  backToTop.hidden = window.scrollY < 500;
  scrollScheduled = false;
};
window.addEventListener('scroll', () => {
  if (scrollScheduled) return;
  scrollScheduled = true;
  window.requestAnimationFrame(updateScroll);
}, { passive: true });
updateScroll();
backToTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: reducedMotion.matches ? 'instant' : 'smooth' });
  const homeLink = document.querySelector('.header .brand');
  homeLink?.focus({ preventScroll: true });
});
