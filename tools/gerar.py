#!/usr/bin/env python3
"""Gera o site estático do Grupo Espaços Vila Olímpia.

Mantém as URLs do WordPress antigo (espacosvilaolimpia.com.br) para não perder
indexação: /listing/<slug>/, /sobre/, /contato/, /orcamento/,
/politica-de-privacidade/ e /restaurant/servicos-de-som-e-iluminacao/.
Também gera sitemap.xml, robots.txt, .htaccess (301/410 no Apache) e páginas
de redirecionamento para hospedagens sem .htaccess (GitHub Pages).

Uso: python3 tools/gerar.py   (rodar na pasta do site)
"""
import html, json, os, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://espacosvilaolimpia.com.br'
BRAND = 'Espaços de eventos'
WA = '5511953116530'
TEL = '+5511981161923'
TEL_TXT = '(11) 98116-1923'
WA_TXT = '(11) 95311-6530'
EMAIL = 'eventos@espacosvilaolimpia.com.br'
HOJE = datetime.date.today().isoformat()
V = '4'  # versão dos assets (cache)

e = lambda s: html.escape(s, quote=True)

# Textos das páginas /listing/ do site original, só com correções de digitação
# ("elettra" no La Fiesta era sobra de outro texto). Não reescrever: é o
# conteúdo indexado.
SPACES = [
    dict(slug='la-fiesta', id='lafiesta', nome='La Fiesta', bairro='Vila Olímpia', end='Rua Alvorada, 1951',
         cap_max=500, fotos=8, capa=3,
         title='La Fiesta, espaço de eventos na Vila Olímpia | Espaços de eventos',
         desc='La Fiesta: espaço para eventos na Vila Olímpia, zona sul de São Paulo, para 100 a 500 pessoas. Som, luz e imagem sem custo adicional. Peça seu orçamento.',
         sub='Espaço de eventos na Vila Olímpia, São Paulo',
         lead='Um dos lounges mais bonitos e sofisticados de São Paulo, perto do Itaim Bibi, do JK Iguatemi e do Shopping Vila Olímpia.',
         facts=['100 a 500 pessoas', 'Corporativo e social', 'Som, luz e imagem inclusos'],
         texto=[
             'O La Fiesta é um espaço para eventos na Vila Olímpia, zona sul de São Paulo, próximo ao bairro do Itaim Bibi, JK Iguatemi, Cidade Jardim, Iguatemi Faria Lima e Shopping Vila Olímpia.',
             'Com localização privilegiada, o La Fiesta é ideal para eventos corporativos, festas sociais, confraternizações e lançamentos, atendendo de 100 a 500 pessoas.',
             'O La Fiesta oferece estrutura completa de som, luz e imagem, sem custo adicional, além de equipe técnica, operacional e gastronômica especializada.',
             'O diferencial do La Fiesta está no atendimento personalizado em todas as etapas, garantindo um evento de alto padrão, com excelência em atendimento, produção e execução.',
             'Lugar perfeito para festas e comemorações. Faça seu evento em um dos lounges mais bonitos e sofisticados de São Paulo.',
         ]),
    dict(slug='vitrinni-corporate', id='vitrinni', nome='Vitrinni Corporate', bairro='Vila Olímpia', end='Rua Quatá, 1',
         fotos=8, capa=2,
         title='Vitrinni Corporate, espaço de eventos na Vila Olímpia | Espaços de eventos',
         desc='Vitrinni Corporate: mais de 700 m² de espaço útil em alto padrão na Vila Olímpia, São Paulo. Eventos corporativos, festas privadas, shows e gravações.',
         sub='Espaço de eventos na Vila Olímpia, zona sul de São Paulo',
         lead='Estrutura adaptável para eventos corporativos, festas privadas, gravações e shows, num lugar moderno e aconchegante.',
         facts=['Mais de 700 m²', 'Alto padrão', 'Shows e gravações'],
         texto=[
             'Vitrinni Corporate, localizado na Vila Olímpia, zona sul de São Paulo. O conforto que seus convidados merecem.',
             'Mais de 700 m² de espaço útil e em alto padrão. Nossa estrutura é completamente adaptável às necessidades de diversos tipos de eventos: desde eventos corporativos a festas privadas, confraternizações, gravação de clipes, eventos culturais, shows, entre outros.',
             'Certamente o público vai se sentir em casa com as comodidades e os ótimos serviços disponíveis em um lugar moderno e aconchegante.',
         ]),
    dict(slug='illustre-gastropub', id='illustre', nome='Illustre Gastropub', bairro='Vila Olímpia', end='Rua Ramos Batista, 491',
         fotos=10, capa=1,
         title='Illustre Gastropub, espaço de eventos na Vila Olímpia | Espaços de eventos',
         desc='Illustre Gastropub: espaço de evento na Vila Olímpia para eventos corporativos e sociais. Melhores drinques, cardápio diferenciado e atendimento premium.',
         sub='Espaço de evento na Vila Olímpia',
         lead='Os melhores drinques, decoração e atendimento premium, com cardápio diferenciado e estrutura completa.',
         facts=['Drinques e cardápio próprio', 'Corporativo e social', 'Melhor custo-benefício'],
         texto=[
             'Illustre Gastropub, para eventos corporativos e sociais. Os melhores drinques, decoração e atendimento premium.',
             'Estrutura completa para o seu evento, cardápio diferenciado e o melhor custo-benefício. Confira agora mesmo.',
             'Rua Ramos Batista, 491, Vila Olímpia, São Paulo.',
         ]),
    dict(slug='espaco-k', id='espacok', nome='Espaço K', bairro='Vila Olímpia', end='Rua Professor Atílio Innocenti',
         fotos=8, capa=2,
         title='Espaço K, espaço de eventos na Vila Olímpia | Espaços de eventos',
         desc='Espaço K: espaço de eventos na Vila Olímpia, zona sul de São Paulo, na mesma quadra da Faria Lima. Moderno e elegante, com segurança e sofisticação.',
         sub='Espaço de eventos na Vila Olímpia, zona sul de São Paulo',
         lead='Na mesma quadra da Faria Lima. Segurança e sofisticação em cada detalhe.',
         facts=['Quadra da Faria Lima', 'Moderno e elegante', 'Corporativo e social'],
         texto=[
             'Espaço de eventos na Vila Olímpia, zona sul de São Paulo, na mesma quadra da Faria Lima.',
             'O Espaço K tem o objetivo de oferecer um lugar perfeito, moderno e elegante para a realização do seu evento, com segurança e sofisticação em cada detalhe.',
         ]),
    dict(slug='notizia', id='notizia', nome='Notizia', bairro='Itaim Bibi', end='Rua Tabapuã, 835',
         cap_max=80, fotos=8, capa=1,
         title='Notizia, espaço de eventos no Itaim Bibi | Espaços de eventos',
         desc='Notizia: espaço de eventos no Itaim Bibi, São Paulo, para até 80 pessoas. Som e iluminação profissional, projeção, open bar e open food.',
         sub='Espaço de eventos no Itaim Bibi',
         lead='Numa vila charmosa do Itaim, entre a Tabapuã e a João Cachoeira. Moderno, aconchegante e versátil.',
         facts=['Até 80 pessoas', 'Projeção multimídia', 'Open bar e open food'],
         texto=[
             'O Notizia é um espaço de eventos localizado no bairro Itaim Bibi, em São Paulo, ideal para quem busca um ambiente moderno, aconchegante e versátil.',
             'Com capacidade para até 80 pessoas, o espaço é perfeito para festas de aniversário, eventos corporativos, confraternizações de fim de ano, reuniões de equipe, lançamentos de produtos e comemorações exclusivas.',
         ],
         lista=('Estrutura completa', [
             'Sistema de som e iluminação profissional',
             'Projeção multimídia para apresentações, vídeos e imagens',
             'Open bar e open food com opções personalizadas',
             'Localização privilegiada em uma vila charmosa no Itaim, com fácil acesso pelas ruas Tabapuã e João Cachoeira',
         ]),
         texto2=['O Notizia oferece toda a infraestrutura necessária para que seu evento seja prático, elegante e inesquecível.']),
    dict(slug='eventos-perdizes-sp', id='perdizes', nome='Eventos Perdizes SP', bairro='Perdizes', end='Rua Diana',
         fotos=8, capa=1,
         title='Eventos Perdizes SP, espaço de eventos em Perdizes | Espaços de eventos',
         desc='Eventos Perdizes SP: espaço para casamentos, aniversários, bodas e eventos corporativos em Perdizes, São Paulo. Pista com palco e área externa coberta.',
         sub='Um lugar único na cidade de São Paulo',
         lead='Informalidade e sofisticação, com pista de dança com palco, salão principal e área externa coberta.',
         facts=['Pista com palco', 'Área externa coberta', 'Casamentos e aniversários'],
         texto=[
             'Somos um grupo com mais de 25 anos no mercado de restaurantes, bares, casas noturnas, restaurantes temáticos e eventos.',
             'O Eventos Perdizes foi criado com um conceito de informalidade e sofisticação, promovendo conforto, elegância e acolhimento aos convidados.',
             'Nossa estrutura possibilita atender diversas demandas de eventos: casamentos, aniversários, bodas, treinamentos corporativos, team building, dentre outros.',
             'O Meu Quintal possui pista de dança com palco, salão principal e área externa com cobertura fixa que remete à lembrança de um quintal, daí o nome.',
             'Atendemos de forma personalizada e exclusiva as necessidades dos nossos clientes. Temos a real e clara responsabilidade em promover seu evento para que seja um sucesso, pois sabemos que nunca é um simples evento, e sim um acontecimento.',
         ]),
]

CLIENTES = [('amazon', 'Amazon'), ('santander', 'Santander'), ('bradesco', 'Bradesco'), ('honda', 'Honda'),
            ('oderbrecht', 'Odebrecht'), ('camargo', 'Camargo Corrêa'), ('olx', 'OLX'), ('imovelweb', 'Imovelweb')]

INCLUI = ['Som', 'Iluminação', 'Imagem', 'Mobiliário', 'Open bar', 'Open food']

ORG_ID = SITE + '/#organizacao'


def wa(msg):
    from urllib.parse import quote
    return f'https://wa.me/{WA}?text={quote(msg)}'


def ordem(s):
    return [s['capa']] + [n for n in range(1, s['fotos'] + 1) if n != s['capa']]


# ---------------------------------------------------------------- moldura

def page(path, title, desc, body, r, *, schema=None, og_img='img/lafiesta-3.jpg', og_type='website', robots=None):
    url = SITE + path
    ld = ''
    for s in (schema or []):
        ld += '<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False, separators=(',', ':')) + '</script>\n'
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
{f'<meta name="robots" content="{robots}">' if robots else '<meta name="robots" content="index, follow, max-image-preview:large">'}
<meta property="og:locale" content="pt_BR">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Grupo Espaços Vila Olímpia">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1d1d2b">
<link rel="icon" href="{r}img/chama.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}styles.css?v={V}">
{ld}</head>
<body data-root="{r}">

<header class="hd">
  <div class="wrap hd-in">
    <a class="logo" href="{r}" aria-label="Grupo Espaços Vila Olímpia, início"><img src="{r}img/logo-180.png" alt="Grupo Espaços Vila Olímpia" width="180" height="55"></a>
    <nav class="nav" id="nav" aria-label="Principal">
      <a href="{r}#espacos">Espaços</a>
      <a href="{r}sobre/">Sobre nós</a>
      <a href="{r}contato/">Contato</a>
    </nav>
    <a class="btn btn-sm" href="{r}orcamento/">Orçamento</a>
    <button class="burger" id="burger" aria-label="Abrir menu" aria-expanded="false" aria-controls="nav"><i></i><i></i><i></i></button>
  </div>
</header>

<main id="top">
{body}
</main>

<footer class="ft">
  <div class="wrap ft-grid">
    <div class="ft-brand">
      <img src="{r}img/logo-180.png" alt="Grupo Espaços Vila Olímpia" width="150" height="46" loading="lazy">
      <p>Espaços para eventos corporativos e sociais em São Paulo.</p>
      <p>Atendimento de segunda a sexta, das 8h às 19h. Visitas apenas com agendamento.</p>
    </div>
    <nav aria-label="Espaços">
      <p class="ft-h">Espaços</p>
      {''.join(f'<a href="{r}listing/{s["slug"]}/">{e(s["nome"])}</a>' for s in SPACES)}
    </nav>
    <nav aria-label="O Grupo">
      <p class="ft-h">O Grupo</p>
      <a href="{r}sobre/">Sobre nós</a>
      <a href="{r}orcamento/">Pré atendimento</a>
      <a href="{r}contato/">Contato</a>
      <a href="{r}restaurant/servicos-de-som-e-iluminacao/">Som e iluminação</a>
      <a href="{r}politica-de-privacidade/">Política de privacidade</a>
    </nav>
    <div>
      <p class="ft-h">Contato imediato</p>
      <a href="{wa('Olá! Vim pelo site e quero saber mais sobre os espaços.')}" target="_blank" rel="noopener">WhatsApp {WA_TXT}</a>
      <a href="tel:{TEL}">Ligar {TEL_TXT}</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
  </div>
  <div class="wrap ft-bottom"><p>© <span id="ano">{datetime.date.today().year}</span> Grupo Espaços Vila Olímpia. Todos os direitos reservados.</p></div>
</footer>

<a class="wa-float" href="{wa('Olá! Vim pelo site.')}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm4.5 12.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>
</a>

<div class="lb" id="lb" hidden>
  <button class="lb-x" id="lbX" aria-label="Fechar">×</button>
  <button class="lb-nav lb-prev" id="lbPrev" aria-label="Foto anterior">‹</button>
  <figure><img id="lbImg" alt=""><figcaption id="lbCap"></figcaption></figure>
  <button class="lb-nav lb-next" id="lbNext" aria-label="Próxima foto">›</button>
</div>

<script src="{r}main.js?v={V}" defer></script>
</body>
</html>
'''


def crumbs(r, items):
    li = [f'<li><a href="{r}">Início</a></li>']
    for name, href in items:
        li.append(f'<li><a href="{href}">{e(name)}</a></li>' if href else f'<li aria-current="page">{e(name)}</li>')
    return '<nav class="crumbs wrap" aria-label="Você está em"><ol>' + ''.join(li) + '</ol></nav>'


def crumbs_ld(items):
    els = [{'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': SITE + '/'}]
    for i, (name, path) in enumerate(items, 2):
        els.append({'@type': 'ListItem', 'position': i, 'name': name, 'item': SITE + path})
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': els}


def address(s):
    return {'@type': 'PostalAddress', 'streetAddress': s['end'], 'addressLocality': 'São Paulo',
            'addressRegion': 'SP', 'addressCountry': 'BR'}


def venue_ld(s):
    d = {'@context': 'https://schema.org', '@type': 'EventVenue', '@id': f'{SITE}/listing/{s["slug"]}/#espaco',
         'name': s['nome'], 'url': f'{SITE}/listing/{s["slug"]}/', 'description': s['desc'],
         'image': [f'{SITE}/img/{s["id"]}-{n}.jpg' for n in ordem(s)[:4]],
         'address': address(s), 'telephone': TEL, 'containedInPlace': {'@type': 'Place', 'name': s['bairro'] + ', São Paulo'},
         'parentOrganization': {'@id': ORG_ID}}
    if s.get('cap_max'):
        d['maximumAttendeeCapacity'] = s['cap_max']
    return d


def card(s, r, eager=False):
    capa = s['capa']
    return f'''
    <article class="card">
      <div class="ph" data-g="{s['id']}" data-n="{s['fotos']}" data-capa="{capa}" data-nome="{e(s['nome'])}">
        <img src="{r}img/sm/{s['id']}-{capa}.webp" width="800" height="600" alt="{e(s['nome'])}, espaço de eventos em {e(s['bairro'])}" loading="{'eager' if eager else 'lazy'}" decoding="async">
        <span class="tag">{e(s['bairro'])}</span>
        <button class="ph-nav ph-prev" aria-label="Foto anterior de {e(s['nome'])}">‹</button>
        <button class="ph-nav ph-next" aria-label="Próxima foto de {e(s['nome'])}">›</button>
        <span class="ph-count">1 / {s['fotos']}</span>
      </div>
      <div class="bd">
        <h3><a href="{r}listing/{s['slug']}/">{e(s['nome'])}</a></h3>
        <p>{e(s['lead'])}</p>
        <ul class="facts">{''.join(f'<li>{e(f)}</li>' for f in s['facts'][:2])}</ul>
        <p class="addr">{PIN}{e(s['end'])}</p>
        <div class="ctas">
          <a class="btn btn-sm btn-line" href="{r}listing/{s['slug']}/" aria-label="Conhecer o {e(s['nome'])}">Conhecer</a>
          <a class="btn btn-sm" href="{wa(f'Olá! Vim pelo site e quero um orçamento no {s["nome"]}.')}" target="_blank" rel="noopener">Orçamento</a>
        </div>
      </div>
    </article>'''


PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
ARROWS = '''<div class="arrows">
        <button class="arr prev" aria-label="Anterior"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>
        <button class="arr next" aria-label="Próximo"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>
      </div>'''


def carrossel_cards(r, titulo, lista, *, h='h2', claro=False, eager=False, auto=True):
    cards = ''.join(card(s, r, eager and i < 3) for i, s in enumerate(lista))
    return f'''<div class="carousel{' on-light' if claro else ''}"{' data-auto' if auto else ''}>
    <div class="wrap row-head"><{h}>{titulo}</{h}>{ARROWS}</div>
    <div class="track track-cards" tabindex="0" aria-label="Carrossel de espaços">{cards}
    </div>
    <div class="dots"></div>
  </div>'''


def write(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


# ---------------------------------------------------------------- páginas

def home():
    r = ''
    body = f'''
<section class="intro">
  <div class="wrap">
    <p class="eyebrow">Vila Olímpia · Itaim Bibi · Perdizes</p>
    <h1>Espaços para eventos em São Paulo</h1>
    <p class="lead">Espaços para eventos corporativos e sociais com som, iluminação, imagem, mobiliário, open bar e open food.</p>
  </div>
</section>

<section class="espacos" id="espacos" aria-label="Espaços">
  {carrossel_cards(r, 'Espaços', SPACES, eager=True)}
</section>

<section class="sobre" id="estrutura">
  <div class="wrap sobre-in">
    <div>
      <p class="eyebrow">Espaços</p>
      <h2>Espaços para eventos</h2>
      <p>Nossos espaços se adaptam ao seu projeto com excelente custo-benefício. Todos os espaços oferecem infraestrutura completa (sistema de som, iluminação, imagens e mobiliário) além de todos os serviços de open bar e open food necessários para realização do evento, seja ele uma festa de confraternização, lançamento de produtos, treinamento ou evento social.</p>
      <p>Localizados em São Paulo, contamos com espaços modernos, sofisticados, despojados e clean, oferecendo aos clientes uma excelente infraestrutura para seus eventos sociais e corporativos.</p>
      <p><a class="link" href="sobre/">Conheça o grupo</a></p>
    </div>
    <ul class="inclui">{''.join(f'<li><b>{x}</b></li>' for x in INCLUI)}</ul>
  </div>
</section>

<section class="clientes" id="clientes">
  <div class="wrap">
    <p class="eyebrow">Alguns clientes</p>
    <h2>Alguns clientes que fazem parte do nosso sucesso</h2>
  </div>
  <div class="marquee">
    <div class="mq">{''.join(f'<img src="img/cli-{k}.jpg" alt="{e(n)}" width="128" height="64" loading="lazy">' for k, n in CLIENTES)}</div>
  </div>
</section>

{contato_bloco(r)}
'''
    org = {'@context': 'https://schema.org', '@type': 'Organization', '@id': ORG_ID, 'name': 'Grupo Espaços Vila Olímpia',
           'alternateName': 'Espaços de eventos SP', 'url': SITE + '/', 'logo': SITE + '/img/logo-180.png', 'email': EMAIL,
           'contactPoint': [{'@type': 'ContactPoint', 'telephone': TEL, 'contactType': 'customer service', 'areaServed': 'BR',
                             'availableLanguage': 'Portuguese', 'hoursAvailable': {'@type': 'OpeningHoursSpecification',
                             'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '08:00', 'closes': '19:00'}}]}
    site = {'@context': 'https://schema.org', '@type': 'WebSite', '@id': SITE + '/#site', 'url': SITE + '/', 'name': BRAND,
            'inLanguage': 'pt-BR', 'publisher': {'@id': ORG_ID}}
    itens = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Espaços para eventos em São Paulo',
             'itemListElement': [{'@type': 'ListItem', 'position': i, 'url': f'{SITE}/listing/{s["slug"]}/', 'name': s['nome']}
                                 for i, s in enumerate(SPACES, 1)]}
    write('index.html', page('/', 'Espaços de eventos em São Paulo | Vila Olímpia, Itaim Bibi e Perdizes',
                             'Espaços para eventos corporativos e sociais em São Paulo: Vila Olímpia, Itaim Bibi e Perdizes. Som, iluminação, imagem, mobiliário, open bar e open food.',
                             body, r, schema=[org, site, itens]))


def contato_bloco(r, h='h2'):
    return f'''<section class="contato" id="contato">
  <div class="wrap contato-in">
    <div>
      <p class="eyebrow">Contato imediato</p>
      <{h}>Vamos marcar uma visita?</{h}>
      <p class="muted">Leo, gerente. Atendimento de segunda a sexta, das 8h às 19h. Visitas apenas com agendamento.</p>
    </div>
    <div class="contato-links">
      <a class="btn btn-wa" href="{wa('Olá! Vim pelo site e quero saber mais sobre os espaços.')}" target="_blank" rel="noopener">WhatsApp {WA_TXT}</a>
      <a class="btn btn-line" href="tel:{TEL}">Ligar {TEL_TXT}</a>
      <a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
  </div>
</section>'''


def listing(s):
    r = '../../'
    path = f'/listing/{s["slug"]}/'
    fotos = ''.join(
        f'<button class="gal-item" data-k="{k}" aria-label="Ampliar foto {k + 1} de {s["fotos"]}"><img src="{r}img/sm/{s["id"]}-{n}.webp" width="800" height="600" alt="{e(s["nome"])}, foto {k + 1}" loading="{"eager" if k < 2 else "lazy"}" decoding="async"></button>'
        for k, n in enumerate(ordem(s)))
    texto = ''.join(f'<p>{e(p)}</p>' for p in s['texto'])
    if s.get('lista'):
        t, itens = s['lista']
        texto += f'<h3>{e(t)}</h3><ul class="ticks">' + ''.join(f'<li>{e(i)}</li>' for i in itens) + '</ul>'
    texto += ''.join(f'<p>{e(p)}</p>' for p in s.get('texto2', []))
    from urllib.parse import quote_plus
    maps = 'https://www.google.com/maps/search/?api=1&amp;query=' + quote_plus(f'{s["end"]}, {s["bairro"]}, São Paulo')
    outros = [x for x in SPACES if x is not s]
    body = f'''
{crumbs(r, [('Espaços', r + '#espacos'), (s['nome'], None)])}

<section class="esp-head">
  <div class="wrap">
    <p class="eyebrow">{e(s['bairro'])} · São Paulo</p>
    <h1>{e(s['nome'])}</h1>
    <p class="lead">{e(s['sub'])}</p>
  </div>
</section>

<section class="gal carousel" data-g="{s['id']}" data-n="{s['fotos']}" data-capa="{s['capa']}" data-nome="{e(s['nome'])}" aria-label="Fotos do {e(s['nome'])}">
  <div class="wrap row-head"><h2>Fotos</h2>{ARROWS}</div>
  <div class="track track-gal" tabindex="0">{fotos}</div>
  <div class="dots"></div>
</section>

<section class="esp-body">
  <div class="wrap esp-grid">
    <article class="prose">
      <h2>Descrição</h2>
      {texto}
      <p class="muted">Peça seu orçamento! Atendimento de segunda a sexta, das 8h às 19h. Visitas apenas com agendamento.</p>
    </article>
    <aside class="esp-card">
      <ul class="facts">{''.join(f'<li>{e(f)}</li>' for f in s['facts'])}</ul>
      <a class="addr" href="{maps}" target="_blank" rel="noopener">{PIN}{e(s['end'])}, {e(s['bairro'])}, São Paulo</a>
      <a class="btn btn-wa" href="{wa(f'Olá! Vim pelo site e quero um orçamento no {s["nome"]}.')}" target="_blank" rel="noopener">Orçamento pelo WhatsApp</a>
      <a class="btn btn-line" href="tel:{TEL}">Ligar {TEL_TXT}</a>
      <a class="btn btn-line" href="{r}orcamento/?espaco={s['slug']}">Pré atendimento online</a>
    </aside>
  </div>
</section>

<section class="outros">
  {carrossel_cards(r, 'Outros espaços', outros, claro=True, auto=False)}
</section>
'''
    write(f'listing/{s["slug"]}/index.html',
          page(path, s['title'], s['desc'], body, r, og_img=f'img/{s["id"]}-{s["capa"]}.jpg',
               schema=[venue_ld(s), crumbs_ld([('Espaços', '/#espacos'), (s['nome'], path)])]))


def simples(path, title, desc, h1, inner, *, eyebrow='', schema=None, extra=''):
    r = '../' * path.strip('/').count('/') + '../'
    body = f'''
{crumbs(r, [(h1, None)])}
<section class="page-head"><div class="wrap">{f'<p class="eyebrow">{e(eyebrow)}</p>' if eyebrow else ''}<h1>{e(h1)}</h1></div></section>
<section class="page-body"><div class="wrap prose">{inner.replace('{r}', r)}</div></section>
{extra.replace('{r}', r)}'''
    write(path.strip('/') + '/index.html', page(path, title, desc, body, r,
                                                schema=(schema or []) + [crumbs_ld([(h1, path)])]))


def sobre():
    inner = f'''
<h2>O que fazemos?</h2>
<p>Somos uma empresa que conecta eventos a espaços. Espaços de eventos SP é um site onde você pode encontrar espaços especiais para seu evento reunidos em uma plataforma única.</p>
<p>Cada um dos espaços disponibilizados possui arquitetura diferenciada e conta com infraestrutura, equipamentos e uma ampla variedade de serviços, proporcionando facilidade e praticidade para os promotores e organizadores de eventos e clientes finais.</p>
<h2>Estrutura completa</h2>
<p>Todos os espaços oferecem infraestrutura completa (sistema de som, iluminação, imagens e mobiliário) além dos serviços de open bar e open food necessários para a realização do evento.</p>
<ul class="ticks">{''.join(f'<li>{x}</li>' for x in INCLUI)}</ul>
<h2>Nossos espaços</h2>
<ul class="ticks">{''.join(f'<li><a href="{{r}}listing/{s["slug"]}/">{e(s["nome"])}</a>, {e(s["bairro"])}</li>' for s in SPACES)}</ul>'''
    simples('/sobre/', 'Sobre nós | Espaços de eventos', 'Somos uma empresa que conecta eventos a espaços: espaços para eventos em São Paulo com arquitetura diferenciada, infraestrutura e serviços completos.',
            'Sobre nós', inner, eyebrow='O Grupo', extra=contato_bloco('{r}'))


def contato():
    inner = f'''
<h2>Entrar em contato</h2>
<p>Fale com o Leo, gerente, pelo WhatsApp ou por telefone. Atendimento de segunda a sexta, das 8h às 19h. Visitas apenas com agendamento.</p>
<div class="contato-cards">
  <a class="cc" href="{wa('Olá! Vim pelo site e quero saber mais sobre os espaços.')}" target="_blank" rel="noopener"><span>WhatsApp</span><b>{WA_TXT}</b></a>
  <a class="cc" href="tel:{TEL}"><span>Ligar</span><b>{TEL_TXT}</b></a>
  <a class="cc" href="mailto:{EMAIL}"><span>E-mail</span><b>{EMAIL}</b></a>
</div>
<p>Prefere mandar os detalhes do evento? Use o <a href="{{r}}orcamento/">pré atendimento online</a>.</p>'''
    simples('/contato/', 'Contato | Espaços de eventos', 'Entre em contato com o Grupo Espaços Vila Olímpia: WhatsApp (11) 95311-6530, telefone (11) 98116-1923 e e-mail. Atendimento de segunda a sexta, das 8h às 19h.',
            'Contato', inner, eyebrow='Contato imediato',
            schema=[{'@context': 'https://schema.org', '@type': 'ContactPage', 'url': SITE + '/contato/', 'about': {'@id': ORG_ID}}])


def orcamento():
    opts = ''.join(f'<option value="{s["slug"]}">{e(s["nome"])}</option>' for s in SPACES)
    inner = f'''
<h2>Orçamento</h2>
<p>Nós te ajudamos a encontrar o melhor espaço! Peça um orçamento 100% online e nossa equipe estará pronta para lhe atender e lhe ajudar na sua melhor escolha.</p>
<form class="orc" id="orc" novalidate>
  <label>Nome<input name="nome" autocomplete="name" required></label>
  <label>Telefone<input name="tel" type="tel" autocomplete="tel" required></label>
  <div class="row2">
    <label>Número de pessoas<input name="pessoas" type="number" min="10" step="1" inputmode="numeric" required></label>
    <label>Data<input name="data" type="date" required></label>
  </div>
  <div class="row2">
    <label>Hora de início<input name="hora" type="time" required></label>
    <label>Já escolheu um espaço?<select name="espaco"><option value="">Ainda não</option>{opts}</select></label>
  </div>
  <label>Descreva seu evento com detalhes<textarea name="desc" rows="4"></textarea></label>
  <p class="hint" id="orcErr" role="alert"></p>
  <button class="btn btn-wa" type="submit">Enviar pelo WhatsApp</button>
  <p class="muted small">Atendimento de segunda a sexta, das 8h às 19h. Visitas apenas com agendamento.</p>
</form>'''
    simples('/orcamento/', 'Pré atendimento e orçamento | Espaços de eventos', 'Peça seu orçamento 100% online: conte o tipo de evento, o número de pessoas e a data, e nós te ajudamos a encontrar o melhor espaço em São Paulo.',
            'Pré atendimento', inner, eyebrow='Orçamento')


def politica():
    out, para = [], []
    for line in (ROOT / 'tools' / 'politica.txt').read_text().splitlines():
        if line.startswith('#'):
            lvl = 'h2' if line.startswith('## ') else 'h3'
            out.append(f'<{lvl}>{e(line.lstrip("# "))}</{lvl}>')
        elif line.strip():
            out.append(f'<p>{e(line.strip())}</p>')
    simples('/politica-de-privacidade/', 'Política de privacidade | Espaços de eventos',
            'Política de privacidade e de cookies do site Espaços de eventos SP, do Grupo Espaços Vila Olímpia.',
            'Política de privacidade', '\n'.join(out))


def artigo_som():
    path = '/restaurant/servicos-de-som-e-iluminacao/'
    paras = [
        'Um serviço de som e iluminação geralmente é contratado para eventos ao vivo, como festas, casamentos, concertos e apresentações corporativas. O objetivo é proporcionar uma experiência sonora e visual agradável e profissional para os participantes do evento.',
        'Os serviços de som geralmente incluem a instalação de alto-falantes, mixers, amplificadores, microfones e outros equipamentos necessários para produzir um som de alta qualidade. O engenheiro de som é responsável por ajustar e mixar o som de acordo com as necessidades do evento.',
        'Já os serviços de iluminação geralmente incluem a instalação de luzes, equipamentos de controle de luz, refletores e outros equipamentos necessários para produzir uma iluminação adequada para o evento. O designer de iluminação é responsável por criar um ambiente visual atraente e adequado às necessidades do evento.',
        'Ambos os serviços devem ser coordenados para garantir que o som e a iluminação estejam sincronizados e criem a atmosfera desejada para o evento. É importante contratar uma empresa profissional e experiente para garantir que o evento seja um sucesso.',
    ]
    inner = '<p class="muted small"><time datetime="2023-04-03">3 de abril de 2023</time></p>' + ''.join(f'<p>{e(p)}</p>' for p in paras) + \
        '<h2>Som e iluminação inclusos nos nossos espaços</h2><p>Todos os nossos espaços já oferecem infraestrutura completa de som, iluminação, imagem e mobiliário. O La Fiesta, por exemplo, oferece som, luz e imagem sem custo adicional.</p><p><a class="btn" href="{r}#espacos">Ver os espaços</a></p>'
    art = {'@context': 'https://schema.org', '@type': 'Article', 'headline': 'Serviços de som e iluminação', 'datePublished': '2023-04-03',
           'inLanguage': 'pt-BR', 'mainEntityOfPage': SITE + path, 'publisher': {'@id': ORG_ID}, 'author': {'@id': ORG_ID}}
    simples(path, 'Serviços de som e iluminação | Espaços de eventos',
            'O que inclui um serviço de som e iluminação para festas, casamentos e eventos corporativos, e por que contratar uma equipe profissional.',
            'Serviços de som e iluminação', inner, eyebrow='Conteúdo', schema=[art])


def pagina_404():
    r = '/'  # 404 é servida em qualquer caminho: caminhos absolutos
    body = f'''<section class="page-head"><div class="wrap"><p class="eyebrow">Erro 404</p><h1>Página não encontrada</h1></div></section>
<section class="page-body"><div class="wrap prose"><p>Essa página não existe mais. Veja nossos espaços:</p>
<ul class="ticks">{''.join(f'<li><a href="/listing/{s["slug"]}/">{e(s["nome"])}</a></li>' for s in SPACES)}</ul></div></section>'''
    write('404.html', page('/404.html', 'Página não encontrada | Espaços de eventos', 'Página não encontrada.', body, r, robots='noindex, follow'))


# ---------------------------------------------------------------- migração

# URLs antigas do WordPress que viram 301 (mesma intenção) e 410 (lixo do tema).
REDIRECT_301 = {
    'home-modern': '/', 'home-static': '/', 'home-static-2': '/', 'dashboard': '/', 'listing-plan/top': '/',
    'listing': '/', 'blog': '/', 'search-v2': '/', 'search-v2-2': '/', 'search-v2-3': '/',
    'taxonomy-template': '/', 'taxonomy-template-2': '/',
    'about-us-2': '/sobre/', 'contact-us-2': '/contato/',
}
GONE_410 = ['pagina-exemplo', 'shop', 'cart', 'checkout', 'checkout-2', 'my-account', 'my-account-2', 'wishlist',
            'add-listing', 'add-listing-plan', 'add-listing-plan-2', 'login', 'login-2', 'term-of-services',
            'become-an-author', 'cancel', 'confirm-account', 'user-plan', 'package', 'planos', 'store-listing',
            'my-orders', 'cadastro']
RESTAURANTES_410 = ['barshu', 'din-tai-fung', 'hakkasan', 'imperial-treasure', 'the-little-lamb', 'my-neighbours-the-dumplings',
                    'the-barbary', 'the-bright', 'padella', 'tapas-brindisa-london-bridge', 'el-pastor', 'hoppers',
                    'tandoor-chop-house', 'the-counter-at-sabor', 'smoking-goat']


def htaccess():
    q = lambda s: s.replace('-', '\\-').replace('.', '\\.')
    r301 = '\n'.join(f'RewriteRule ^{q(k)}/?$ {v}? [R=301,L]' for k, v in REDIRECT_301.items())
    gone = '|'.join(q(x) for x in GONE_410)
    rest = '|'.join(q(x) for x in RESTAURANTES_410)
    write('.htaccess', f'''# Grupo Espaços Vila Olímpia: site estático que substitui o WordPress.
# Gerado por tools/gerar.py. Não remover a pasta wp-content/uploads do servidor:
# as fotos antigas podem estar indexadas no Google Imagens.

Options -MultiViews -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html
ErrorDocument 410 /404.html

<IfModule mod_rewrite.c>
RewriteEngine On

# Domínio único: https, sem www
RewriteCond %{{HTTPS}} off [OR]
RewriteCond %{{HTTP_HOST}} ^www\\. [NC]
RewriteRule ^ https://espacosvilaolimpia.com.br%{{REQUEST_URI}} [R=301,L,NE]

# Links curtos do WordPress (?p=123, ?page_id=123) e feeds
RewriteCond %{{QUERY_STRING}} (^|&)(p|page_id)=\\d+ [NC]
RewriteRule ^$ /? [R=301,L]
RewriteRule ^(.*/)?feed/?$ /? [R=301,L]
RewriteRule ^comments/feed/?$ /? [R=301,L]

# Sitemaps antigos do WordPress apontam para o novo
RewriteRule ^wp-sitemap(-[a-z0-9_-]+)?\\.xml$ /sitemap.xml [R=301,L]
RewriteRule ^sitemap_index\\.xml$ /sitemap.xml [R=301,L]

# Páginas antigas com a mesma intenção (301)
{r301}

# Restos do tema WordPress sem relação com o negócio (410 Gone)
RewriteRule ^({gone})/?$ - [G,L]
RewriteRule ^restaurant/({rest})/?$ - [G,L]
RewriteRule ^(listing_location|listing_cat|listing_tag|listing_plan)/ - [G,L]
RewriteRule ^wp-(login\\.php|admin|json)(/.*)?$ - [G,L]
</IfModule>

<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml application/xml text/xml
</IfModule>

<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType text/html "access plus 0 seconds"
ExpiresByType text/css "access plus 1 month"
ExpiresByType application/javascript "access plus 1 month"
ExpiresByType image/jpeg "access plus 6 months"
ExpiresByType image/webp "access plus 6 months"
ExpiresByType image/png "access plus 6 months"
</IfModule>
''')


def stubs():
    """Para hospedagem sem .htaccess (GitHub Pages): meta refresh imediato + canonical."""
    for k, v in REDIRECT_301.items():
        dest = SITE + v
        write(f'{k}/index.html', f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Redirecionando</title>
<link rel="canonical" href="{dest}">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={'../' * (k.count('/') + 1)}{v.lstrip('/')}">
</head><body><p><a href="{dest}">Continuar para {dest}</a></p></body></html>
''')
    # GitHub Pages não redireciona .xml: o wp-sitemap.xml vira um índice que aponta para o novo
    write('wp-sitemap.xml', f'''<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>{SITE}/sitemap.xml</loc></sitemap></sitemapindex>
''')


def sitemap():
    urls = [('/', '1.0')] + [(f'/listing/{s["slug"]}/', '0.9') for s in SPACES] + \
           [('/orcamento/', '0.7'), ('/contato/', '0.7'), ('/sobre/', '0.6'),
            ('/restaurant/servicos-de-som-e-iluminacao/', '0.4'), ('/politica-de-privacidade/', '0.2')]
    imgs = {f'/listing/{s["slug"]}/': s for s in SPACES}
    out = []
    for u, pr in urls:
        im = ''
        if u in imgs:
            s = imgs[u]
            im = ''.join(f'<image:image><image:loc>{SITE}/img/{s["id"]}-{n}.jpg</image:loc></image:image>' for n in ordem(s))
        out.append(f'<url><loc>{SITE}{u}</loc><lastmod>{HOJE}</lastmod><priority>{pr}</priority>{im}</url>')
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
          + '\n'.join(out) + '\n</urlset>\n')
    write('robots.txt', f'User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {SITE}/sitemap.xml\n')


if __name__ == '__main__':
    home()
    for s in SPACES:
        listing(s)
    sobre(); contato(); orcamento(); politica(); artigo_som(); pagina_404()
    htaccess(); stubs(); sitemap()
    print('ok')
