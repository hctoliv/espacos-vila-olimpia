# Migração SEO: WordPress → site estático

Site: https://espacosvilaolimpia.com.br (hoje WordPress + Elementor + tema de diretório, Apache)
Novo: esta pasta, gerada por `python3 tools/gerar.py`. Preview: https://hctoliv.github.io/espacos-vila-olimpia/

Auditoria feita em 05/11/2026. **Sem acesso ao Search Console**: não há dado real de cliques ou posições.
A estratégia foi preservar tudo que pode estar indexado e trazer tráfego, e eliminar só o que é lixo do tema.

## O que foi feito

| URL original | Antes (WordPress) | Agora | Status |
|---|---|---|---|
| `/` | title "Espaços de eventos – São Paulo", sem H1, sem description, cards via JS | title + description + H1, 6 cards em HTML com link para cada espaço, schema Organization/WebSite/ItemList | 200 |
| `/listing/la-fiesta/` | title "LA FIESTA – Espaços de eventos", H1 "LA FIESTA Atualizado", sem description | mesma URL, texto original integral (corrigido "elettra"), H1 limpo, description, galeria, schema EventVenue + Breadcrumb | 200 |
| `/listing/vitrinni-corporate/` | idem | idem | 200 |
| `/listing/illustre-gastropub/` | idem | idem | 200 |
| `/listing/espaco-k/` | idem | idem | 200 |
| `/listing/notizia/` | idem | idem (lista "Estrutura completa" mantida) | 200 |
| `/listing/eventos-perdizes-sp/` | idem | idem | 200 |
| `/sobre/` | "O que fazemos?" | mesma URL, mesmo texto + lista dos espaços (links internos) | 200 |
| `/contato/` | formulário + Leo gerente | mesma URL, WhatsApp/telefone/e-mail | 200 |
| `/orcamento/` | formulário de pré atendimento | mesma URL, mesmo formulário (envia pelo WhatsApp) | 200 |
| `/politica-de-privacidade/` | texto legal | mesma URL, mesmo texto | 200 |
| `/restaurant/servicos-de-som-e-iluminacao/` | artigo de 2023 | mesma URL, mesmo artigo + link para os espaços | 200 |
| `/home-static/`, `/home-static-2/`, `/home-modern/`, `/dashboard/`, `/listing-plan/top/`, `/listing/`, `/blog/`, `/search-v2*/`, `/taxonomy-template*/` | duplicatas da home / buscas com erro 500 | → `/` (meta refresh + canonical; 301 no Apache) | ok |
| `/about-us-2/` · `/contact-us-2/` | páginas demo | → `/sobre/` · `/contato/` (meta refresh + canonical) | ok |
| `/wp-sitemap.xml` e sub-sitemaps | sitemap WP com 72 URLs (10 com erro 500) | índice apontando para `/sitemap.xml` (12 páginas reais + 50 imagens) | ok |
| `/feed/`, `?page_id=` | feeds e links curtos WP | `/feed/` → `/`; `?page_id=` cai na home (canonical `/`) | ok |
| `/cart/`, `/shop/`, `/login/`… (23 páginas) e 15 `/restaurant/` de Londres | lixo do tema | 404 no GitHub Pages (410 se for para Apache) | 404 |
| `http://` e `www.` | http não redirecionava (conteúdo duplicado) | 301 → `https://espacosvilaolimpia.com.br` (feito pelo GitHub) | 301 |

Outras melhorias: canonical absoluto em todas as páginas, Open Graph completo, rodapé com links para os 6 espaços
(o antigo apontava para 4 buscas com erro 500), fotos dos cards em WebP de 800px (≈50 KB em vez de ≈250 KB),
página 404 útil, cópia das 289 fotos antigas em `wp-content/uploads/` (mesmas URLs).

Cobertura do texto original nas páginas dos espaços: 94 a 100% das palavras.

## Hospedagem escolhida: GitHub Pages (repo hctoliv/espacos-vila-olimpia, branch main)

Diferenças em relação a um Apache, já tratadas:
- GitHub Pages não faz 301. As URLs antigas com destino (home-static, about-us-2, feed…) têm uma página com
  meta refresh imediato + canonical, que o Google trata como redirecionamento permanente.
- Sem 410: o lixo do tema responde 404 (o Google remove do índice do mesmo jeito, só um pouco mais devagar).
- Os sitemaps do WordPress (`wp-sitemap*.xml`) viraram índices que apontam para o `/sitemap.xml`.
- As 289 fotos antigas do WordPress (62 MB) estão copiadas em `wp-content/uploads/` nos mesmos caminhos,
  então nenhuma URL de imagem indexada quebra.
- `www` → raiz e `http` → `https` o próprio GitHub faz, depois do passo 4.
- O `.htaccess` fica no repo só para o caso de um dia o site ir para um Apache; o GitHub ignora.

## ⚠️ O e-mail roda no servidor atual

`eventos@espacosvilaolimpia.com.br` usa MX → `mail.espacosvilaolimpia.com.br` → 162.241.203.20 (o mesmo servidor do WordPress,
DNS em ns1/ns2.guiadorossi.com.br). Por isso:
- **Mudar só** o registro A da raiz e o `www`. **Não mexer** em MX, `mail`, TXT (SPF) nem em outros subdomínios.
- **Não cancelar a hospedagem atual**, senão o e-mail para.

## Passo a passo do lançamento

1. **Backup completo do WordPress** (arquivos + banco) no painel da hospedagem. É o rollback.
2. Confirmar com o cliente os números da Rua Quatá (site antigo "1", BaresSP 1016 para o Vitrinni Lounge), da Rua Diana
   (Perdizes) e da Rua Professor Atílio Innocenti (Espaço K). Corrigir em `tools/gerar.py`, rodar e publicar.
3. **Um dia antes**: no DNS (cPanel › Zone Editor), baixar o TTL dos registros `espacosvilaolimpia.com.br` (A) e `www` de 14400 para 300.
   Opcional, recomendado: verificar o domínio no GitHub (Settings › Pages › Verified domains), que pede um TXT `_github-pages-challenge-hctoliv`.
4. **No dia**, no DNS:
   | Nome | Tipo | Valor |
   |---|---|---|
   | `espacosvilaolimpia.com.br` | A | 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 (4 registros, apagar o 162.241.203.20) |
   | `espacosvilaolimpia.com.br` | AAAA | 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153 |
   | `www` | CNAME | `hctoliv.github.io` |
   | `mail`, MX, TXT, demais | — | **não mexer** |
5. Logo depois, apontar o Pages para o domínio (cria o arquivo CNAME no repo):
   ```bash
   gh api -X PUT repos/hctoliv/espacos-vila-olimpia/pages -f cname=espacosvilaolimpia.com.br
   ```
   A partir daqui `hctoliv.github.io/espacos-vila-olimpia` redireciona para o domínio.
6. Esperar o certificado (minutos a algumas horas; em Settings › Pages aparece "certificate active") e então marcar **Enforce HTTPS**:
   ```bash
   gh api -X PUT repos/hctoliv/espacos-vila-olimpia/pages -F https_enforced=true
   ```
7. Conferir (abaixo) e mandar um e-mail de teste para eventos@ para confirmar que continua chegando.
8. Search Console: enviar `/sitemap.xml`, remover o `wp-sitemap.xml`, pedir indexação da home e das 6 páginas `/listing/`,
   testar 2 páginas no Teste de pesquisa aprimorada (schema).

## Conferência depois do lançamento

```bash
for u in / /listing/la-fiesta/ /listing/notizia/ /sobre/ /orcamento/ /sitemap.xml /wp-content/uploads/2021/09/16-1024x774-1.jpeg; do
  printf "%-60s " $u; curl -s -o /dev/null -w "%{http_code}\n" https://espacosvilaolimpia.com.br$u; done
curl -s https://espacosvilaolimpia.com.br/home-static/ | grep -o 'canonical" href="[^"]*'
curl -sI http://www.espacosvilaolimpia.com.br/ | grep -iE "^HTTP|location"
dig +short MX espacosvilaolimpia.com.br; dig +short mail.espacosvilaolimpia.com.br
```

Esperado: 200 em tudo da primeira linha; `/home-static/` com canonical para `/`; `www`/`http` com 301 para
`https://espacosvilaolimpia.com.br/`; MX e `mail` ainda em 162.241.203.20.

## GEO (buscadores com IA: ChatGPT, Perplexity, AI Overviews do Google, Copilot)

O que já está no site (gerado por `tools/gerar.py`, sem nenhum fato inventado):
- **Resumo no topo de cada espaço** ("Em resumo: …") em uma frase autossuficiente, fácil de citar.
- **Ficha rápida** por espaço: endereço, capacidade (só onde o original informa; nos outros "Sob consulta"), eventos, estrutura, destaques, atendimento.
- **Perguntas frequentes** em cada espaço (5) e na home (7), com schema `FAQPage`.
- **Comparativo** na home: os 6 espaços lado a lado (bairro, capacidade, ideal para).
- **Clientes em texto** (não só logos): Amazon, Santander, Bradesco, Honda, Odebrecht, Camargo Corrêa, OLX e Imovelweb.
- **Entidade**: `Organization` com descrição (25 anos de mercado), `areaServed`, `knowsAbout` e os 6 `EventVenue` ligados;
  cada espaço com `amenityFeature`, `keywords`, `hasMap`, `WebPage.dateModified`.
- **`/llms.txt`**: resumo do grupo, dos espaços e das perguntas, em Markdown, para assistentes de IA.
- **`robots.txt`** liberando explicitamente GPTBot, OAI-SearchBot, ChatGPT-User, PerplexityBot, ClaudeBot, Claude-SearchBot,
  Google-Extended, Applebot-Extended, Bingbot e DuckAssistBot. Se o cliente não quiser que o conteúdo treine modelos,
  tirar só GPTBot, ClaudeBot, Google-Extended e Applebot-Extended (os de busca continuam e a citação não é afetada).
- **IndexNow**: chave `357eaf7eeca013f0a6e54743cb55866e` (arquivo `/357eaf7eeca013f0a6e54743cb55866e.txt`). Avisa Bing/Copilot e Yandex na hora; o ChatGPT busca muito pelo índice do Bing.

Depois do lançamento:
1. **Bing Webmaster Tools**: importar o site do Search Console e enviar o `/sitemap.xml`.
2. Avisar o IndexNow (repetir sempre que mudar conteúdo):
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" -X POST https://api.indexnow.org/indexnow -H "Content-Type: application/json" -d '{"host":"espacosvilaolimpia.com.br","key":"357eaf7eeca013f0a6e54743cb55866e","urlList":["https://espacosvilaolimpia.com.br/","https://espacosvilaolimpia.com.br/listing/la-fiesta/","https://espacosvilaolimpia.com.br/listing/vitrinni-corporate/","https://espacosvilaolimpia.com.br/listing/illustre-gastropub/","https://espacosvilaolimpia.com.br/listing/espaco-k/","https://espacosvilaolimpia.com.br/listing/notizia/","https://espacosvilaolimpia.com.br/listing/eventos-perdizes-sp/","https://espacosvilaolimpia.com.br/llms.txt"]}'
   ```
   (200 ou 202 = recebido.)
3. **Fora do site, onde as IAs mais buscam confirmação** (precisa do cliente):
   - Perfil da Empresa no Google para cada espaço, com o mesmo nome, endereço e telefone do site.
   - Corrigir os diretórios antigos: o BaresSP lista "Vitrinni Lounge" na Rua Quatá, 1016, e La Fiesta sem dados novos.
   - Instagram do grupo/espaços: quando tiver o @, colocar em `sameAs` no schema (`tools/gerar.py`, objeto `org`).
   - Avaliações no Google: a IA cita muito "bem avaliado" a partir delas.
4. **Medir**: uma vez por mês, perguntar no ChatGPT, Perplexity e Google (AI Overview) coisas como
   "espaço para eventos na Vila Olímpia para 300 pessoas", "espaço para confraternização no Itaim Bibi até 80 pessoas",
   "espaço para casamento em Perdizes" e anotar se o site ou o espaço aparece e é citado. No GA4 (quando instalado),
   acompanhar visitas de origem chatgpt.com, perplexity.ai, copilot.microsoft.com e gemini.google.com.

Para manter: a data "Informações atualizadas em" (`ATUALIZADO` em `tools/gerar.py`) deve mudar quando os dados mudarem.

## Monitoramento (30 dias)

| Quando | O que olhar | Sinal de alerta |
|---|---|---|
| Dia 1 a 3 | Search Console › Páginas: erros 5xx/404 inesperados; Inspeção de URL das 6 `/listing/` | qualquer `/listing/` fora do índice |
| Semana 1 | Desempenho: cliques e impressões por página vs. as 4 semanas antes | queda de mais de 30% numa página com volume relevante |
| Semana 2 | Cobertura: 410s saindo do índice, sitemap processado sem erro | URLs boas marcadas como "rastreada, não indexada" |
| Semana 4 | Posição média das consultas de marca e de "espaço de eventos vila olímpia/itaim" | perda de posição persistente (não oscilação de 1 a 2 dias) |
| Contínuo | Core Web Vitals (relatório do Search Console) e cliques no WhatsApp (GA4, se instalado) | LCP > 2,5 s no mobile |

Comparar sempre com o mesmo período anterior (sazonalidade de fim de ano pesa muito para eventos corporativos).

## Rollback

O WordPress continua instalado no servidor. Se algo der errado: voltar o registro A da raiz para 162.241.203.20 e o `www` para CNAME `espacosvilaolimpia.com.br`
(com TTL 300, volta em minutos) e tirar o domínio do Pages com `gh api -X PUT repos/hctoliv/espacos-vila-olimpia/pages -f cname=`.

## Como editar

Todo o conteúdo está em `tools/gerar.py` (lista `SPACES`). Editou, rode `python3 tools/gerar.py` na pasta do site.
Não edite os `index.html` à mão: são sobrescritos.
