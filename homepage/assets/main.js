// career-log · main.js
(function(){
  // Theme toggle
  const key = 'career-log-theme';
  const saved = localStorage.getItem(key);
  if (saved) document.documentElement.dataset.theme = saved;
  document.getElementById('theme-toggle').addEventListener('click', () => {
    const now = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = now;
    localStorage.setItem(key, now);
    setupVanta(); // rerun with new colors
  });

  // Number counter on stats
  const nums = document.querySelectorAll('.stat-value');
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseFloat(el.dataset.target);
      const dur = 1200;
      const start = performance.now();
      function tick(now) {
        const p = Math.min(1, (now - start) / dur);
        const eased = 1 - Math.pow(1 - p, 3);
        const v = target * eased;
        el.textContent = target < 10 ? v.toFixed(0) : Math.round(v).toLocaleString();
        if (p < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
      io.unobserve(el);
    });
  }, { threshold: 0.5 });
  nums.forEach(n => io.observe(n));

  // Load resume manifest and render timeline
  fetch('resume/manifest.json')
    .then(r => r.json())
    .then(manifest => {
      const list = document.getElementById('resume-list');
      const sorted = manifest.snapshots.sort((a,b) => b.date.localeCompare(a.date));
      list.innerHTML = sorted.map(s => `
        <a class="resume-item" href="resume/${s.date}-general.pdf" download>
          <div>
            <div class="date">${s.date}</div>
            <div class="meta">${s.badge || ('入职第 ' + s.day + ' 天')}</div>
          </div>
          <span class="dl">↓ PDF</span>
        </a>
      `).join('');
      // Update last snap
      if (sorted[0]) {
        document.getElementById('last-snap').textContent = sorted[0].date;
        const f = document.getElementById('last-snap-footer');
        if (f) f.textContent = sorted[0].date;
        document.getElementById('days-in').textContent = '入职第 ' + sorted[0].day + ' 天';
      }
    })
    .catch(() => {
      const list = document.getElementById('resume-list');
      list.innerHTML = '<p style="color:var(--fg-muted)">（快照 manifest 尚未生成，请稍后刷新）</p>';
    });

  // Vanta.js NET background
  function setupVanta() {
    if (window._vanta) { window._vanta.destroy(); }
    if (typeof VANTA === 'undefined' || typeof THREE === 'undefined') { return setTimeout(setupVanta, 200); }
    const dark = document.documentElement.dataset.theme !== 'light';
    window._vanta = VANTA.NET({
      el: '#bg',
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: dark ? 0x4c8bf5 : 0x1f3a5f,
      backgroundColor: dark ? 0x0a0f1e : 0xfafbfc,
      points: 12.00,
      maxDistance: 22.00,
      spacing: 18.00,
      showDots: true
    });
  }
  setupVanta();

  // Smooth anchor scroll (native scroll-behavior handles most)
  document.querySelectorAll('nav a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      const id = a.getAttribute('href').slice(1);
      const el = document.getElementById(id);
      if (el) window.scrollTo({ top: el.offsetTop - 60, behavior: 'smooth' });
    });
  });
})();
