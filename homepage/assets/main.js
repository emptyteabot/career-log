// career-log · v3 · particles + i18n + live card
(function () {
  // ===== I18N =====
  const key = 'career-log-lang';
  const saved = localStorage.getItem(key) || 'zh';
  applyLang(saved);
  document.getElementById('lang-toggle').addEventListener('click', () => {
    const next = document.documentElement.dataset.lang === 'zh' ? 'en' : 'zh';
    applyLang(next);
    localStorage.setItem(key, next);
  });
  function applyLang(lang) {
    document.documentElement.dataset.lang = lang;
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
    document.getElementById('lang-toggle').textContent = lang === 'zh' ? 'EN' : '中';
    document.querySelectorAll('[data-i18n-zh]').forEach(el => {
      const text = el.getAttribute('data-i18n-' + lang);
      if (text) el.innerHTML = text;
    });
  }

  // ===== Verdict diagram =====
  const diagram = document.getElementById('verdict-diagram');
  if (diagram) {
    diagram.textContent = [
      '$ arkcli-eval run --host claude-code --version v12',
      '',
      '  L1 preflight ─────────▶ ok',
      '     env  ok · tenant scope ok · login ok',
      '  L2 exec ──────────────▶ ok',
      '     cmd run · exit 0 · 2.3 s',
      '  L3 output assert ─────▶ regex pass',
      '     schema ok · json valid',
      '',
      '  ────────────────────────────────────',
      '  v10 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  100.0 %',
      '  v11 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░   97.6 %',
      '  v12 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░   79.2 %  ← fixing',
    ].join('\n');
  }

  // ===== Live time =====
  const tf = new Intl.DateTimeFormat('en-CA', {
    hour: '2-digit', minute: '2-digit',
    year: 'numeric', month: '2-digit', day: '2-digit',
    timeZone: 'Asia/Shanghai', hour12: false,
  });
  function tickTime() {
    const el = document.getElementById('live-time');
    if (!el) return;
    const parts = tf.formatToParts(new Date());
    const get = t => parts.find(p => p.type === t)?.value;
    el.textContent = `${get('year')}-${get('month')}-${get('day')} ${get('hour')}:${get('minute')} CST`;
  }
  tickTime(); setInterval(tickTime, 30000);

  // ===== Live progress fills =====
  requestAnimationFrame(() => {
    const daysFill = document.getElementById('days-fill');
    if (daysFill) daysFill.style.width = (47 / 183 * 100).toFixed(1) + '%';
  });

  // ===== Archive from manifest =====
  fetch('resume/manifest.json').then(r => r.json()).then(m => {
    const list = document.getElementById('archive-list');
    const sorted = [...m.snapshots].sort((a, b) => b.date.localeCompare(a.date));
    const last = sorted[0];
    if (last) {
      document.getElementById('last-snap').textContent = last.date;
      const days = document.getElementById('days-in-hero'); if (days) days.textContent = last.day;
    }
    if (list) list.innerHTML = sorted.map(s => `
      <li>
        <a href="resume/${s.date}-general.pdf" download>${s.date}</a>
        <span class="a-badge">${s.badge ? s.badge.substring(0, 22) : 'day ' + s.day}</span>
      </li>`).join('');
  }).catch(() => {});

  // ===== Particle grid background =====
  const canvas = document.getElementById('grid-bg');
  const ctx = canvas.getContext('2d');
  let W = 0, H = 0, DPR = Math.min(window.devicePixelRatio || 1, 2);
  const mouse = { x: -9999, y: -9999, active: false };
  const nodes = [];
  const density = 0.00007; // nodes per pixel
  const linkDist = 140;

  function resize() {
    W = window.innerWidth; H = window.innerHeight;
    canvas.width = W * DPR; canvas.height = H * DPR;
    canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    // (Re)populate nodes
    const target = Math.max(60, Math.floor(W * H * density));
    if (nodes.length < target) {
      while (nodes.length < target) nodes.push(spawnNode());
    } else if (nodes.length > target) {
      nodes.length = target;
    }
  }
  function spawnNode() {
    return {
      x: Math.random() * W,
      y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.25,
      vy: (Math.random() - 0.5) * 0.25,
      r: Math.random() * 1.4 + 0.6,
      hue: Math.random() < 0.15 ? 'accent' : 'base',
    };
  }
  window.addEventListener('resize', resize);
  window.addEventListener('mousemove', e => {
    mouse.x = e.clientX; mouse.y = e.clientY; mouse.active = true;
  });
  window.addEventListener('mouseout', () => { mouse.active = false; });

  function step() {
    ctx.clearRect(0, 0, W, H);
    // subtle gradient overlay
    const g = ctx.createRadialGradient(W * 0.7, H * 0.3, 100, W * 0.7, H * 0.3, Math.max(W, H));
    g.addColorStop(0, 'rgba(88,166,255,0.045)');
    g.addColorStop(1, 'rgba(88,166,255,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);

    // move
    for (const n of nodes) {
      n.x += n.vx; n.y += n.vy;
      if (n.x < 0 || n.x > W) n.vx *= -1;
      if (n.y < 0 || n.y > H) n.vy *= -1;
      // mouse attraction
      if (mouse.active) {
        const dx = mouse.x - n.x, dy = mouse.y - n.y;
        const d2 = dx * dx + dy * dy;
        if (d2 < 200 * 200 && d2 > 1) {
          const f = 40 / d2;
          n.vx += dx * f * 0.001;
          n.vy += dy * f * 0.001;
        }
      }
      // damping
      n.vx *= 0.995; n.vy *= 0.995;
    }

    // draw links
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i], b = nodes[j];
        const dx = a.x - b.x, dy = a.y - b.y;
        const d = Math.hypot(dx, dy);
        if (d < linkDist) {
          const alpha = (1 - d / linkDist) * 0.18;
          ctx.strokeStyle = `rgba(88,166,255,${alpha})`;
          ctx.lineWidth = 0.7;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }
    // nodes
    for (const n of nodes) {
      ctx.beginPath();
      ctx.fillStyle = n.hue === 'accent' ? 'rgba(163,113,247,0.85)' : 'rgba(88,166,255,0.65)';
      ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
      ctx.fill();
    }
    requestAnimationFrame(step);
  }
  resize();
  step();
})();
