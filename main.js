(() => {
  const WA = '5511953116530';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const ROOT = document.body.dataset.root || '';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Galerias: data-g (prefixo das fotos), data-n (quantidade), data-capa (primeira)
  const order = el => {
    const n = +el.dataset.n, capa = +el.dataset.capa;
    return [capa, ...Array.from({ length: n }, (_, k) => k + 1).filter(k => k !== capa)];
  };
  const sm = (g, n) => `${ROOT}img/sm/${g}-${n}.webp`;
  const big = (g, n) => `${ROOT}img/${g}-${n}.jpg`;

  /* ---------- carrosséis ---------- */
  $$('.carousel').forEach(box => {
    const track = $('.track', box), dots = $('.dots', box), items = [...track.children];
    if (!items.length) return;
    const step = () => items[0].offsetWidth + parseFloat(getComputedStyle(track).columnGap || 0);
    const current = () => Math.round(track.scrollLeft / step());
    const maxStart = () => Math.max(0, Math.round((track.scrollWidth - track.clientWidth) / step()));
    const go = i => {
      const last = maxStart();
      if (i > last) i = 0;
      if (i < 0) i = last;
      track.scrollTo({ left: i * step(), behavior: reduce ? 'auto' : 'smooth' });
    };
    items.forEach((_, i) => dots.insertAdjacentHTML('beforeend', `<button aria-label="Ir para o item ${i + 1}" data-i="${i}"></button>`));
    const dotBtns = $$('button', dots);
    const sync = () => {
      const c = Math.min(current(), maxStart());
      dotBtns.forEach((b, k) => { b.hidden = k > maxStart(); b.classList.toggle('on', k === c); });
      $$('.arr', box).forEach(a => a.hidden = maxStart() === 0);
    };
    let raf;
    track.addEventListener('scroll', () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(sync); }, { passive: true });
    addEventListener('resize', sync);
    sync();

    let paused = false, timer;
    const auto = box.hasAttribute('data-auto') && !reduce;
    const hold = () => { clearInterval(timer); if (auto) timer = setInterval(() => { if (!paused && !document.hidden && $('#lb').hidden) go(current() + 1); }, 5500); };
    $('.prev', box).addEventListener('click', () => { go(current() - 1); hold(); });
    $('.next', box).addEventListener('click', () => { go(current() + 1); hold(); });
    dots.addEventListener('click', e => { const b = e.target.closest('button'); if (b) { go(+b.dataset.i); hold(); } });
    track.addEventListener('pointerenter', () => paused = true);
    track.addEventListener('pointerleave', () => paused = false);
    track.addEventListener('touchstart', hold, { passive: true });
    track.addEventListener('focusin', () => paused = true);
    track.addEventListener('focusout', () => paused = false);
    track.addEventListener('keydown', e => {
      if (e.target !== track) return;
      if (e.key === 'ArrowRight') { go(current() + 1); hold(); }
      if (e.key === 'ArrowLeft') { go(current() - 1); hold(); }
    });
    hold();
  });

  /* ---------- fotos dentro do card ---------- */
  $$('.ph').forEach(ph => {
    const list = order(ph), img = $('img', ph), count = $('.ph-count', ph);
    let k = 0;
    const set = i => {
      k = (i + list.length) % list.length;
      img.src = sm(ph.dataset.g, list[k]);
      count.textContent = `${k + 1} / ${list.length}`;
    };
    ph.addEventListener('click', e => {
      if (e.target.closest('.ph-prev')) return set(k - 1);
      if (e.target.closest('.ph-next')) return set(k + 1);
      openLb(ph, k);
    });
  });

  /* ---------- galeria em tela cheia ---------- */
  const lb = $('#lb'), lbImg = $('#lbImg'), lbCap = $('#lbCap');
  let lbEl = null, lbK = 0, lastFocus = null;
  const lbShow = () => {
    const list = order(lbEl);
    lbK = (lbK + list.length) % list.length;
    lbImg.src = big(lbEl.dataset.g, list[lbK]);
    lbImg.alt = `${lbEl.dataset.nome}, foto ${lbK + 1}`;
    lbCap.textContent = `${lbEl.dataset.nome} · ${lbK + 1} / ${list.length}`;
  };
  const openLb = (el, k) => {
    lbEl = el; lbK = k; lastFocus = document.activeElement;
    lbShow(); lb.hidden = false; document.body.style.overflow = 'hidden'; $('#lbX').focus();
  };
  const closeLb = () => { lb.hidden = true; document.body.style.overflow = ''; lastFocus && lastFocus.focus(); };
  $('#lbX').addEventListener('click', closeLb);
  $('#lbPrev').addEventListener('click', () => { lbK--; lbShow(); });
  $('#lbNext').addEventListener('click', () => { lbK++; lbShow(); });
  lb.addEventListener('click', e => { if (e.target === lb) closeLb(); });
  addEventListener('keydown', e => {
    if (lb.hidden) return;
    if (e.key === 'Escape') closeLb();
    if (e.key === 'ArrowLeft') { lbK--; lbShow(); }
    if (e.key === 'ArrowRight') { lbK++; lbShow(); }
  });
  let tx = null;
  lb.addEventListener('touchstart', e => tx = e.touches[0].clientX, { passive: true });
  lb.addEventListener('touchend', e => {
    if (tx === null) return;
    const dx = e.changedTouches[0].clientX - tx; tx = null;
    if (Math.abs(dx) > 40) { lbK += dx < 0 ? 1 : -1; lbShow(); }
  });

  // página do espaço: cada foto da faixa abre a galeria
  const gal = $('.gal');
  if (gal) gal.addEventListener('click', e => {
    const b = e.target.closest('.gal-item'); if (b) openLb(gal, +b.dataset.k);
  });

  /* ---------- pré atendimento ---------- */
  const orc = $('#orc');
  if (orc) {
    const pre = new URLSearchParams(location.search).get('espaco');
    if (pre) orc.espaco.value = pre;
    orc.addEventListener('submit', e => {
      e.preventDefault();
      const f = orc.elements, err = $('#orcErr');
      const falta = ['nome', 'tel', 'pessoas', 'data', 'hora'].filter(n => !f[n].value.trim());
      if (falta.length) { err.textContent = 'Preencha nome, telefone, número de pessoas, data e hora.'; f[falta[0]].focus(); return; }
      if (+f.pessoas.value < 10) { err.textContent = 'O número de pessoas precisa ser 10 ou mais.'; f.pessoas.focus(); return; }
      err.textContent = '';
      const data = f.data.value.split('-').reverse().join('/');
      const esp = f.espaco.value ? f.espaco.options[f.espaco.selectedIndex].text : 'ainda não escolhi';
      const msg = [
        'Olá! Vim pelo site e quero um orçamento.',
        `Nome: ${f.nome.value.trim()}`,
        `Telefone: ${f.tel.value.trim()}`,
        `Pessoas: ${f.pessoas.value}`,
        `Data: ${data} às ${f.hora.value}`,
        `Espaço: ${esp}`,
        f.desc.value.trim() && `Evento: ${f.desc.value.trim()}`,
      ].filter(Boolean).join('\n');
      window.open(`https://wa.me/${WA}?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
    });
  }

  /* ---------- menu ---------- */
  const burger = $('#burger'), nav = $('#nav');
  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });
  nav.addEventListener('click', e => { if (e.target.closest('a')) { nav.classList.remove('open'); burger.setAttribute('aria-expanded', false); } });

  // logos duplicados pro loop contínuo
  const mq = $('.mq');
  if (mq) mq.innerHTML += mq.innerHTML.replace(/alt="[^"]*"/g, 'alt="" aria-hidden="true"');
})();
