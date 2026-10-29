(() => {
  const WA = '5511953116530';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // Dados dos espaços (textos e endereços do site espacosvilaolimpia.com.br)
  const SPACES = [
    { id: 'lafiesta', nome: 'La Fiesta', bairro: 'Vila Olímpia', end: 'Rua Alvorada, 1951', acc: 'var(--c5)',
      lead: 'Um dos lounges mais bonitos e sofisticados de São Paulo, perto do Itaim Bibi, do JK Iguatemi e do Shopping Vila Olímpia. Equipe técnica, operacional e gastronômica própria e atendimento personalizado em todas as etapas.',
      facts: ['100 a 500 pessoas', 'Som, luz e imagem sem custo adicional', 'Corporativo e social'], hot: 0,
      min: 100, max: 500, fotos: 8, hero: 3, alt: 2, casamento: true },
    { id: 'vitrinni', nome: 'Vitrinni Corporate', bairro: 'Vila Olímpia', end: 'Rua Quatá, 1', acc: 'var(--c4)',
      lead: 'O conforto que seus convidados merecem. Estrutura adaptável para eventos corporativos, festas privadas, confraternizações, gravação de clipes, eventos culturais e shows, num lugar moderno e aconchegante.',
      facts: ['Mais de 700 m² de espaço útil', 'Alto padrão', 'Shows e gravações'], hot: 0,
      fotos: 8, hero: 2, alt: 3, casamento: true },
    { id: 'illustre', nome: 'Illustre Gastropub', bairro: 'Vila Olímpia', end: 'Rua Ramos Batista, 491', acc: 'var(--c3)',
      lead: 'Os melhores drinques, decoração e atendimento premium. Cardápio diferenciado e estrutura completa para eventos corporativos e sociais, com o melhor custo-benefício.',
      facts: ['Os melhores drinques', 'Cardápio diferenciado', 'Atendimento premium'], hot: 0,
      fotos: 10, hero: 1, alt: 2, casamento: true },
    { id: 'espacok', nome: 'Espaço K', bairro: 'Vila Olímpia', end: 'Rua Professor Atílio Innocenti', acc: 'var(--c2)',
      lead: 'Na mesma quadra da Faria Lima. Um lugar moderno e elegante para o seu evento, com segurança e sofisticação em cada detalhe.',
      facts: ['Na quadra da Faria Lima', 'Casamentos e corporativos', 'Moderno e elegante'], hot: 0,
      fotos: 8, hero: 2, alt: 3, casamento: true },
    { id: 'notizia', nome: 'Notizia', bairro: 'Itaim Bibi', end: 'Rua Tabapuã, 835', acc: 'var(--c1)',
      lead: 'Numa vila charmosa do Itaim, entre a Tabapuã e a João Cachoeira. Moderno, aconchegante e versátil, com som e iluminação profissional, projeção multimídia, open bar e open food.',
      facts: ['Até 80 pessoas', 'Projeção multimídia', 'Aniversários e reuniões'], hot: 0,
      max: 80, fotos: 8, hero: 1, alt: 2, casamento: false },
    { id: 'perdizes', nome: 'Eventos Perdizes', bairro: 'Perdizes', end: 'Rua Diana', acc: 'var(--c6)',
      lead: 'Informalidade e sofisticação, com conforto, elegância e acolhimento. Pista de dança com palco, salão principal e área externa com cobertura fixa que lembra um quintal.',
      facts: ['Pista com palco', 'Área externa coberta', 'Casamentos, aniversários e bodas'], hot: 2,
      fotos: 8, hero: 1, alt: 3, casamento: true },
  ];
  const img = (s, n) => `img/${s.id}-${n}.jpg`;
  const pad = n => String(n).padStart(2, '0');

  /* ---------- intro ---------- */
  const intro = $('#intro');
  let seen = false;
  try { seen = sessionStorage.getItem('evo-intro') === '1'; } catch (e) {}
  const start = () => document.body.classList.add('ready');
  if (seen || matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('no-intro'); start();
  } else {
    const end = () => {
      if (intro.classList.contains('out')) return;
      intro.classList.add('out'); start();
      try { sessionStorage.setItem('evo-intro', '1'); } catch (e) {}
      setTimeout(() => intro.remove(), 1100);
    };
    setTimeout(end, 2300);
    intro.addEventListener('click', end);
    addEventListener('keydown', end, { once: true });
  }

  /* ---------- hero ---------- */
  const heroBg = $('#heroBg'), heroList = $('#heroList'), heroNow = $('#heroNow');
  SPACES.forEach((s, i) => {
    const im = new Image();
    im.src = img(s, s.hero); im.alt = ''; im.decoding = 'async';
    if (i > 0) im.loading = 'lazy';
    heroBg.append(im);
    heroList.insertAdjacentHTML('beforeend',
      `<li><button type="button" data-i="${i}"><span class="n">${pad(i + 1)}</span><span class="nm">${s.nome}</span><span class="bq">${s.bairro}</span><i class="bar"></i></button></li>`);
  });
  let cur = -1, timer;
  const DUR = 6000;
  heroList.style.setProperty('--dur', DUR + 'ms');
  const show = i => {
    cur = (i + SPACES.length) % SPACES.length;
    $$('img', heroBg).forEach((im, k) => { if (k === cur) im.loading = 'eager'; im.classList.toggle('on', k === cur); });
    $$('li', heroList).forEach((li, k) => {
      li.classList.remove('on');
      if (k === cur) { void li.offsetWidth; li.classList.add('on'); }
    });
    heroNow.textContent = `${pad(cur + 1)} / ${pad(SPACES.length)} · ${SPACES[cur].nome}`;
    clearTimeout(timer); timer = setTimeout(() => show(cur + 1), DUR);
  };
  heroList.addEventListener('click', e => {
    const b = e.target.closest('button'); if (b) show(+b.dataset.i);
  });
  show(0);

  /* ---------- manifesto: palavras acendem com o scroll ---------- */
  const big = $('#bigWords');
  const hlFrom = big.textContent.indexOf('conecta'), hlTo = big.textContent.indexOf('.') + 1;
  let pos = 0;
  big.innerHTML = big.textContent.split(' ').map(w => {
    const s = pos; pos += w.length + 1;
    return `<span class="w${s >= hlFrom && s < hlTo ? ' hl' : ''}">${w}</span>`;
  }).join(' ');
  const words = $$('.w', big);

  /* ---------- contadores ---------- */
  const countIO = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    countIO.unobserve(e.target);
    const el = e.target, to = +el.dataset.count, pre = el.dataset.pre || '', suf = el.dataset.suf || '';
    const t0 = performance.now();
    const step = t => {
      const p = Math.min(1, (t - t0) / 1400), v = Math.round(to * (1 - Math.pow(1 - p, 3)));
      el.textContent = pre + v.toLocaleString('pt-BR') + suf;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }), { threshold: .6 });
  $$('[data-count]').forEach(el => countIO.observe(el));

  /* ---------- cards dos espaços ---------- */
  const stack = $('#stack');
  SPACES.forEach((s, i) => {
    const thumbs = [1, 2, 3, 4].map(n => n === s.hero ? s.fotos : n).slice(0, 4)
      .map(n => `<button type="button" data-s="${i}" data-n="${n}" aria-label="Foto ${n} de ${s.nome}"><img src="${img(s, n)}" alt="" loading="lazy"></button>`).join('');
    stack.insertAdjacentHTML('beforeend', `
      <article class="card" style="--i:${i};--acc:${s.acc}" id="esp-${s.id}">
        <div class="card-media" data-s="${i}" data-n="${s.hero}" role="button" tabindex="0" aria-label="Ver fotos de ${s.nome}">
          <img src="${img(s, s.hero)}" alt="${s.nome}" loading="lazy">
          <img class="alt" src="${img(s, s.alt)}" alt="" loading="lazy">
          <span class="tag">${s.bairro}</span>
          <span class="zoom">${s.fotos} fotos ↗</span>
        </div>
        <div class="card-body">
          <div class="idx mono"><span>${pad(i + 1)} / ${pad(SPACES.length)}<i></i></span><span>${s.bairro}</span></div>
          <h3>${s.nome}</h3>
          <p class="lead">${s.lead}</p>
          <ul class="facts">${s.facts.map((f, k) => `<li${k === s.hot ? ' class="hot"' : ''}>${f}</li>`).join('')}</ul>
          <div class="thumbs">${thumbs}</div>
          <div class="card-cta">
            <a class="btn btn-sm" href="#orcamento" data-pick="${s.id}">Quero este espaço</a>
            <a class="addr" href="https://www.google.com/maps/search/${encodeURIComponent(s.end + ', ' + s.bairro + ', São Paulo')}" target="_blank" rel="noopener">${s.end}</a>
          </div>
        </div>
      </article>`);
  });
  const cards = $$('.card', stack);

  /* ---------- lightbox ---------- */
  const lb = $('#lb'), lbImg = $('#lbImg'), lbCap = $('#lbCap');
  let lbS = 0, lbN = 1;
  const lbShow = () => {
    const s = SPACES[lbS];
    lbImg.src = img(s, lbN); lbImg.alt = s.nome;
    lbCap.textContent = `${s.nome} · ${lbN} / ${s.fotos}`;
  };
  const lbOpen = (si, n) => { lbS = si; lbN = n; lbShow(); lb.hidden = false; document.body.style.overflow = 'hidden'; };
  const lbClose = () => { lb.hidden = true; document.body.style.overflow = ''; };
  const lbGo = d => { const f = SPACES[lbS].fotos; lbN = ((lbN - 1 + d + f) % f) + 1; lbShow(); };
  stack.addEventListener('click', e => {
    const t = e.target.closest('[data-n]'); if (t) lbOpen(+t.dataset.s, +t.dataset.n);
  });
  stack.addEventListener('keydown', e => {
    if (e.key === 'Enter' && e.target.matches('.card-media')) lbOpen(+e.target.dataset.s, +e.target.dataset.n);
  });
  $('#lbX').onclick = lbClose;
  $('#lbPrev').onclick = () => lbGo(-1);
  $('#lbNext').onclick = () => lbGo(1);
  lb.addEventListener('click', e => { if (e.target === lb) lbClose(); });
  addEventListener('keydown', e => {
    if (lb.hidden) return;
    if (e.key === 'Escape') lbClose();
    if (e.key === 'ArrowRight') lbGo(1);
    if (e.key === 'ArrowLeft') lbGo(-1);
  });
  let tx = 0;
  lb.addEventListener('touchstart', e => { tx = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', e => { const d = e.changedTouches[0].clientX - tx; if (Math.abs(d) > 40) lbGo(d < 0 ? 1 : -1); });

  /* ---------- planner ---------- */
  const TIPOS = ['Corporativo', 'Confraternização', 'Lançamento de produto', 'Treinamento', 'Aniversário', 'Casamento', 'Outro'];
  const st = { tipo: '', guests: 120, pick: '' };
  const tiposEl = $('#tipos'), picks = $('#picks'), guests = $('#guests'), gOut = $('#gOut');
  tiposEl.innerHTML = TIPOS.map(t => `<button type="button" aria-pressed="false">${t}</button>`).join('');
  tiposEl.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    const on = b.getAttribute('aria-pressed') !== 'true';
    $$('button', tiposEl).forEach(x => x.setAttribute('aria-pressed', 'false'));
    b.setAttribute('aria-pressed', String(on));
    st.tipo = on ? b.textContent : '';
    update();
  });
  picks.innerHTML = SPACES.map(s =>
    `<button type="button" class="pick" data-id="${s.id}" aria-pressed="false"><img src="${img(s, s.hero)}" alt="" loading="lazy"><i class="badge"></i><span>${s.nome}<small>${s.bairro}</small></span></button>`).join('') +
    `<button type="button" class="pick any" data-id="" aria-pressed="false"><span>Ainda não sei,<br>me ajudem a escolher</span></button>`;
  picks.addEventListener('click', e => {
    const b = e.target.closest('.pick'); if (!b) return;
    st.pick = b.getAttribute('aria-pressed') === 'true' ? '' : (b.dataset.id || 'ajuda');
    update();
  });
  const fit = s => {
    if (st.tipo === 'Casamento' && !s.casamento) return [false, 'outro perfil'];
    if (s.max && st.guests > s.max) return [false, `até ${s.max} pessoas`];
    if (s.min && st.guests < s.min) return [false, `a partir de ${s.min}`];
    return [true, s.min || s.max ? 'cabe' : 'indicado'];
  };
  const setRange = () => {
    st.guests = +guests.value; gOut.textContent = st.guests;
    guests.style.setProperty('--p', ((st.guests - 10) / 490 * 100) + '%');
  };
  guests.addEventListener('input', () => { setRange(); update(); });

  const fmtDate = v => v ? v.split('-').reverse().join('/') : '';
  const val = id => $('#' + id).value.trim();
  const update = () => {
    let ok = 0;
    $$('.pick', picks).forEach(b => {
      const id = b.dataset.id;
      b.setAttribute('aria-pressed', String(id ? st.pick === id : st.pick === 'ajuda'));
      if (!id) return;
      const [f, label] = fit(SPACES.find(s => s.id === id));
      b.classList.toggle('no', !f); $('.badge', b).textContent = label; if (f) ok++;
    });
    $('#pickHint').textContent = `${ok} de ${SPACES.length} espaços indicados para ${st.guests} convidados${st.tipo ? ' · ' + st.tipo.toLowerCase() : ''}. Toque para escolher.`;
    const sp = SPACES.find(s => s.id === st.pick);
    const rows = [
      ['Evento', st.tipo],
      ['Convidados', String(st.guests)],
      ['Data', fmtDate(val('data'))],
      ['Início', val('hora')],
      ['Espaço', sp ? sp.nome : st.pick === 'ajuda' ? 'Quero ajuda' : ''],
      ['Nome', val('nome')],
    ];
    $('#ticket').innerHTML = rows.map(([k, v]) => `<dt>${k}</dt><dd class="${v ? '' : 'empty'}">${v || '—'}</dd>`).join('');
  };
  ['data', 'hora', 'nome', 'empresa', 'desc'].forEach(id => $('#' + id).addEventListener('input', update));
  $('#data').min = new Date().toISOString().slice(0, 10);
  $('#tNum').textContent = '#' + String(Date.now()).slice(-5);

  // "Quero este espaço" nos cards
  document.addEventListener('click', e => {
    const a = e.target.closest('[data-pick]'); if (!a) return;
    st.pick = a.dataset.pick; update();
  });

  $('#planner').addEventListener('submit', e => {
    e.preventDefault();
    const nome = $('#nome');
    if (!nome.value.trim()) { nome.classList.add('err'); nome.focus(); return; }
    nome.classList.remove('err');
    const sp = SPACES.find(s => s.id === st.pick);
    const L = [
      `Olá, Leo! Sou ${val('nome')}${val('empresa') ? ' (' + val('empresa') + ')' : ''} e quero um orçamento.`,
      '',
      st.tipo ? `• Evento: ${st.tipo}` : null,
      `• Convidados: ${st.guests}`,
      val('data') ? `• Data: ${fmtDate(val('data'))}` : null,
      val('hora') ? `• Início: ${val('hora')}` : null,
      `• Espaço: ${sp ? sp.nome + ' (' + sp.bairro + ')' : 'ainda não sei, quero ajuda pra escolher'}`,
      val('desc') ? `• Detalhes: ${val('desc')}` : null,
    ].filter(x => x !== null);
    window.open(`https://wa.me/${WA}?text=${encodeURIComponent(L.join('\n'))}`, '_blank', 'noopener');
  });
  setRange(); update();

  /* ---------- onde estamos ---------- */
  const end = $('#enderecos'), oImg = $('#ondeImg'), oCap = $('#ondeCap');
  end.innerHTML = SPACES.map((s, i) =>
    `<li style="--acc:${s.acc}" data-i="${i}"><a href="https://www.google.com/maps/search/${encodeURIComponent(s.end + ', ' + s.bairro + ', São Paulo')}" target="_blank" rel="noopener"><b>${s.nome}</b><span>${s.end} · ${s.bairro}</span><em>mapa ↗</em></a></li>`).join('');
  const setOnde = i => {
    const s = SPACES[i];
    $$('li', end).forEach((li, k) => li.classList.toggle('on', k === i));
    oImg.src = img(s, s.alt); oCap.textContent = `${s.nome} · ${s.bairro}`;
  };
  end.addEventListener('mouseover', e => { const li = e.target.closest('li'); if (li) setOnde(+li.dataset.i); });
  setOnde(0);

  /* ---------- status de atendimento (horário de SP) ---------- */
  const status = $('#status');
  const sp = new Date(new Date().toLocaleString('en-US', { timeZone: 'America/Sao_Paulo' }));
  const open = sp.getDay() >= 1 && sp.getDay() <= 5 && sp.getHours() >= 8 && sp.getHours() < 19;
  status.classList.toggle('open', open);
  $('span', status).textContent = open ? 'Atendendo agora' : 'Fora do horário, deixe sua mensagem';
  $('#ano').textContent = new Date().getFullYear();

  /* ---------- reveals ---------- */
  $$('.sec-head, .inclui li, .stat, .enderecos li, .contato-grid > div, .pl-step, .pl-ticket').forEach((el, i) => {
    el.classList.add('rv'); el.style.transitionDelay = (i % 3) * 70 + 'ms';
  });
  const rvIO = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); rvIO.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px' });
  $$('.rv').forEach(el => rvIO.observe(el));

  /* ---------- menu ---------- */
  const hd = $('#hd'), nav = $('#nav'), burger = $('#burger');
  const menu = on => {
    nav.classList.toggle('open', on); hd.classList.toggle('menu', on);
    burger.setAttribute('aria-expanded', String(on));
    document.body.style.overflow = on ? 'hidden' : '';
  };
  burger.onclick = () => menu(!nav.classList.contains('open'));
  nav.addEventListener('click', e => { if (e.target.closest('a')) menu(false); });

  /* ---------- scroll (um único rAF) ---------- */
  const lightZones = $$('[data-hd=light]'), fab = $('.wa-float'), planner = $('#orcamento'), manifesto = $('#sobre');
  let lastY = 0, ticking = false;
  const onScroll = () => {
    ticking = false;
    const y = scrollY, vh = innerHeight;
    hd.classList.toggle('solid', y > 40);
    if (!nav.classList.contains('open')) hd.classList.toggle('hide', y > lastY && y > vh * .8);
    lastY = y;
    const probe = 34;
    hd.classList.toggle('on-light', lightZones.some(z => { const r = z.getBoundingClientRect(); return r.top <= probe && r.bottom >= probe; }));
    const pr = planner.getBoundingClientRect();
    fab.classList.toggle('show', y > vh * .9 && !(pr.top < vh && pr.bottom > 0));

    // manifesto
    const mr = big.getBoundingClientRect();
    const p = Math.min(1, Math.max(0, (vh * .85 - mr.top) / (mr.height + vh * .35)));
    const n = Math.round(p * words.length);
    words.forEach((w, k) => w.classList.toggle('lit', k < n));

    // cards: o de baixo empurra o de cima pra trás
    cards.forEach((c, k) => {
      const next = cards[k + 1];
      if (!next) return;
      const nr = next.getBoundingClientRect(), cr = c.getBoundingClientRect();
      const q = Math.min(1, Math.max(0, 1 - (nr.top - cr.top) / cr.height));
      c.style.transform = q ? `scale(${1 - q * .05})` : '';
      c.style.filter = q ? `brightness(${1 - q * .45})` : '';
    });
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  addEventListener('resize', onScroll);
  onScroll();
})();
