// career-log · main.js · minimalist · i18n only
(function () {
  const key = 'career-log-lang';
  const saved = localStorage.getItem(key) || 'zh';
  applyLang(saved);
  const btn = document.getElementById('lang-toggle');
  if (btn) btn.addEventListener('click', () => {
    const next = document.documentElement.dataset.lang === 'zh' ? 'en' : 'zh';
    applyLang(next);
    localStorage.setItem(key, next);
  });
  function applyLang(lang) {
    document.documentElement.dataset.lang = lang;
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
    const b = document.getElementById('lang-toggle');
    if (b) b.textContent = lang === 'zh' ? 'EN' : '中';
    document.querySelectorAll('[data-i18n-zh]').forEach(el => {
      const text = el.getAttribute('data-i18n-' + lang);
      if (text) el.innerHTML = text;
    });
  }

  // Smooth anchor scroll offset for sticky nav
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href').slice(1);
      if (!id) return;
      const el = document.getElementById(id);
      if (!el) return;
      e.preventDefault();
      window.scrollTo({ top: el.offsetTop - 70, behavior: 'smooth' });
    });
  });
})();
