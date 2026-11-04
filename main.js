(() => {
  const WA = '5511953116530';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // Textos e endereços do site espacosvilaolimpia.com.br
  const SPACES = [
    { id: 'lafiesta', nome: 'La Fiesta', bairro: 'Vila Olímpia', end: 'Rua Alvorada, 1951',
      lead: 'Um dos lounges mais bonitos e sofisticados de São Paulo, perto do Itaim Bibi, do JK Iguatemi e do Shopping Vila Olímpia.',
      facts: ['100 a 500 pessoas', 'Corporativo e social'], fotos: 8, capa: 3 },
    { id: 'vitrinni', nome: 'Vitrinni Corporate', bairro: 'Vila Olímpia', end: 'Rua Quatá, 1',
      lead: 'Estrutura adaptável para eventos corporativos, festas privadas, gravações e shows, num lugar moderno e aconchegante.',
      facts: ['Mais de 700 m²', 'Alto padrão'], fotos: 8, capa: 2 },
    { id: 'illustre', nome: 'Illustre Gastropub', bairro: 'Vila Olímpia', end: 'Rua Ramos Batista, 491',
      lead: 'Os melhores drinques, decoração e atendimento premium, com cardápio diferenciado e estrutura completa.',
      facts: ['Drinques autorais', 'Corporativo e social'], fotos: 10, capa: 1 },
    { id: 'espacok', nome: 'Espaço K', bairro: 'Vila Olímpia', end: 'Rua Professor Atílio Innocenti',
      lead: 'Na mesma quadra da Faria Lima. Segurança e sofisticação em cada detalhe.',
      facts: ['Quadra da Faria Lima', 'Moderno e elegante'], fotos: 8, capa: 2 },
    { id: 'notizia', nome: 'Notizia', bairro: 'Itaim Bibi', end: 'Rua Tabapuã, 835',
      lead: 'Numa vila charmosa do Itaim, entre a Tabapuã e a João Cachoeira. Moderno, aconchegante e versátil.',
      facts: ['Até 80 pessoas', 'Projeção multimídia'], fotos: 8, capa: 1 },
    { id: 'perdizes', nome: 'Eventos Perdizes', bairro: 'Perdizes', end: 'Rua Diana',
      lead: 'Informalidade e sofisticação, com pista de dança com palco, salão principal e área externa coberta.',
      facts: ['Pista com palco', 'Área externa'], fotos: 8, capa: 1 },
  ];
  const img = (s, n) => `img/${s.id}-${n}.jpg`;
  const order = s => [s.capa, ...Array.from({ length: s.fotos }, (_, k) => k + 1).filter(n => n !== s.capa)];
  const waLink = s => `https://wa.me/${WA}?text=${encodeURIComponent(`Olá! Vim pelo site e quero um orçamento no ${s.nome}.`)}`;
  const pin = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>';

  /* ---------- cards ---------- */
  const track = $('#track'), dots = $('#dots');
  SPACES.forEach((s, i) => {
    track.insertAdjacentHTML('beforeend', `
      <article class="card" data-i="${i}">
        <div class="ph" data-s="${i}">
          <img src="${img(s, s.capa)}" alt="${s.nome}" loading="${i < 3 ? 'eager' : 'lazy'}">
          <span class="tag">${s.bairro}</span>
          <button class="ph-nav ph-prev" aria-label="Foto anterior">‹</button>
          <button class="ph-nav ph-next" aria-label="Próxima foto">›</button>
          <span class="ph-count">1 / ${s.fotos}</span>
        </div>
        <div class="bd">
          <h3>${s.nome}</h3>
          <p>${s.lead}</p>
          <ul class="facts">${s.facts.map(f => `<li>${f}</li>`).join('')}</ul>
          <a class="addr" href="https://www.google.com/maps/search/${encodeURIComponent(s.end + ', ' + s.bairro + ', São Paulo')}" target="_blank" rel="noopener">${pin}${s.end}</a>
          <div class="ctas">
            <a class="btn btn-sm" href="${waLink(s)}" target="_blank" rel="noopener">Pedir orçamento</a>
            <button class="btn btn-sm btn-line" data-fotos="${i}">Ver fotos</button>
          </div>
        </div>
      </article>`);
    dots.insertAdjacentHTML('beforeend', `<button aria-label="Ir para ${s.nome}" data-i="${i}"></button>`);
  });
  const cards = $$('.card', track), dotBtns = $$('button', dots);

  // foto dentro do card
  const photoIdx = SPACES.map(() => 0);
  const setPhoto = (i, k) => {
    const s = SPACES[i], list = order(s);
    photoIdx[i] = (k + list.length) % list.length;
    const card = cards[i];
    $('.ph img', card).src = img(s, list[photoIdx[i]]);
    $('.ph-count', card).textContent = `${photoIdx[i] + 1} / ${s.fotos}`;
  };

  /* ---------- carrossel ---------- */
  const step = () => cards[0].offsetWidth + parseFloat(getComputedStyle(track).columnGap || 0);
  const current = () => Math.round(track.scrollLeft / step());
  const maxStart = () => Math.round((track.scrollWidth - track.clientWidth) / step());
  const go = i => {
    const last = maxStart();
    if (i > last) i = 0;
    if (i < 0) i = last;
    track.scrollTo({ left: i * step(), behavior: 'smooth' });
  };
  $('#prev').addEventListener('click', () => { go(current() - 1); hold(); });
  $('#next').addEventListener('click', () => { go(current() + 1); hold(); });
  dots.addEventListener('click', e => { const b = e.target.closest('button'); if (b) { go(+b.dataset.i); hold(); } });
  const syncDots = () => {
    const c = current();
    dotBtns.forEach((b, k) => {
      b.hidden = k > maxStart();
      b.classList.toggle('on', k === Math.min(c, maxStart()));
    });
  };
  let raf;
  track.addEventListener('scroll', () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(syncDots); }, { passive: true });
  addEventListener('resize', syncDots);
  syncDots();

  // avanço automático, pausa quando a pessoa mexe
  let paused = false, timer;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const tick = () => { if (!paused && !document.hidden) go(current() + 1); };
  const hold = () => { clearInterval(timer); if (!reduce) timer = setInterval(tick, 5500); };
  track.addEventListener('pointerenter', () => paused = true);
  track.addEventListener('pointerleave', () => paused = false);
  track.addEventListener('touchstart', hold, { passive: true });
  track.addEventListener('focusin', () => paused = true);
  track.addEventListener('focusout', () => paused = false);
  track.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') { go(current() + 1); hold(); }
    if (e.key === 'ArrowLeft') { go(current() - 1); hold(); }
  });
  hold();

  track.addEventListener('click', e => {
    const card = e.target.closest('.card'); if (!card) return;
    const i = +card.dataset.i;
    if (e.target.closest('.ph-prev')) return setPhoto(i, photoIdx[i] - 1);
    if (e.target.closest('.ph-next')) return setPhoto(i, photoIdx[i] + 1);
    if (e.target.closest('[data-fotos]')) return openLb(i, 0);
    if (e.target.closest('.ph')) return openLb(i, photoIdx[i]);
  });

  /* ---------- galeria ---------- */
  const lb = $('#lb'), lbImg = $('#lbImg'), lbCap = $('#lbCap');
  let lbS = 0, lbK = 0;
  const lbShow = () => {
    const s = SPACES[lbS], list = order(s);
    lbK = (lbK + list.length) % list.length;
    lbImg.src = img(s, list[lbK]); lbImg.alt = s.nome;
    lbCap.textContent = `${s.nome} · ${lbK + 1} / ${s.fotos}`;
  };
  const openLb = (i, k) => { lbS = i; lbK = k; lbShow(); lb.hidden = false; document.body.style.overflow = 'hidden'; paused = true; $('#lbX').focus(); };
  const closeLb = () => { lb.hidden = true; document.body.style.overflow = ''; paused = false; };
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

  /* ---------- menu ---------- */
  const burger = $('#burger'), nav = $('#nav');
  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });
  nav.addEventListener('click', e => { if (e.target.closest('a')) { nav.classList.remove('open'); burger.setAttribute('aria-expanded', false); } });

  // logos duplicados pro loop contínuo
  const mq = $('.mq');
  mq.innerHTML += mq.innerHTML.replace(/alt="[^"]*"/g, 'alt="" aria-hidden="true"');

  $('#ano').textContent = new Date().getFullYear();
})();
