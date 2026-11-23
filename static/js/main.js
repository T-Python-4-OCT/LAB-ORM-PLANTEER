// Header shadow + back-to-top button
const header = document.querySelector('.site-header');
const backToTop = document.querySelector('.back-to-top');
const onScroll = () => {
  const y = window.scrollY;
  header.classList.toggle('scrolled', y > 8);
  backToTop.classList.toggle('show', y > 500);
};
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();
backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// Toasts: close button + auto-dismiss
document.querySelectorAll('.toast').forEach((toast) => {
  const close = () => {
    toast.classList.add('hide');
    setTimeout(() => toast.remove(), 300);
  };
  toast.querySelector('.toast-close').addEventListener('click', close);
  setTimeout(close, 4500);
});

// Reveal sections and cards on scroll
const revealTargets = document.querySelectorAll('.reveal, .grid .card, .category-tile, .message-card');
if ('IntersectionObserver' in window) {
  revealTargets.forEach((el, i) => {
    el.classList.add('will-reveal');
    el.style.transitionDelay = `${(i % 3) * 80}ms`;
  });
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const el = entry.target;
        el.classList.add('revealed');
        observer.unobserve(el);
        setTimeout(() => { el.style.transitionDelay = ''; }, 800);
      }
    });
  }, { threshold: 0.1 });
  revealTargets.forEach((el) => observer.observe(el));
}

// Count-up numbers in the stats strip
document.querySelectorAll('[data-count]').forEach((el) => {
  const target = parseInt(el.dataset.count, 10) || 0;
  const start = performance.now();
  const duration = 900;
  const tick = (now) => {
    const p = Math.min((now - start) / duration, 1);
    el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
    if (p < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
});

// Live image preview on the add / update plant form
const imageInput = document.querySelector('input[type=file][name=image]');
if (imageInput) {
  const preview = document.createElement('img');
  preview.className = 'image-preview';
  preview.alt = 'Preview';
  const current = document.querySelector('.field a[href*="/media/"]');
  if (current) preview.src = current.href;
  else preview.hidden = true;
  imageInput.closest('.field').appendChild(preview);
  imageInput.addEventListener('change', () => {
    const file = imageInput.files[0];
    if (file) {
      preview.src = URL.createObjectURL(file);
      preview.hidden = false;
    }
  });
}

// Close the mobile menu after picking a link
document.querySelectorAll('.nav-links a').forEach((a) =>
  a.addEventListener('click', () => { document.getElementById('nav-toggle').checked = false; })
);
