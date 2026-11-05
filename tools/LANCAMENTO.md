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
| `/home-static/`, `/home-static-2/`, `/home-modern/`, `/dashboard/`, `/listing-plan/top/`, `/listing/`, `/blog/`, `/search-v2*/`, `/taxonomy-template*/` | duplicatas da home / buscas com erro 500 | 301 → `/` | 301 |
| `/about-us-2/` · `/contact-us-2/` | páginas demo | 301 → `/sobre/` · `/contato/` | 301 |
| `/wp-sitemap.xml` e sub-sitemaps | sitemap WP com 72 URLs (10 com erro 500) | 301 → `/sitemap.xml` (12 páginas reais + 50 imagens) | 301 |
| `?p=`, `?page_id=`, `/feed/` | links curtos e feeds WP | 301 → `/` | 301 |
| `/cart/`, `/shop/`, `/login/`… (23 páginas) e 15 `/restaurant/` de Londres | lixo do tema | 410 Gone | 410 |
| `http://` e `www.` | http não redirecionava (conteúdo duplicado) | 301 → `https://espacosvilaolimpia.com.br` | 301 |

Outras melhorias: canonical absoluto em todas as páginas, Open Graph completo, rodapé com links para os 6 espaços
(o antigo apontava para 4 buscas com erro 500), fotos dos cards em WebP de 800px (≈50 KB em vez de ≈250 KB),
página 404 útil, gzip e cache no `.htaccess`.

Cobertura do texto original nas páginas dos espaços: 94 a 100% das palavras.

## Antes de apontar o domínio (obrigatório)

1. **Backup completo do WordPress** (arquivos + banco) pelo painel da hospedagem. É o rollback.
2. **Hospedagem**: subir no mesmo Apache (recomendado). O `.htaccess` faz os 301/410 de verdade.
   No GitHub Pages não existe 301: os redirecionamentos viram meta refresh (pasta de cada URL antiga) e os 410 viram 404.
3. Na raiz do servidor: remover os arquivos do WordPress e **manter `wp-content/uploads/`** (fotos antigas podem estar no Google Imagens).
   Não precisa subir `tools/` nem `.git/` (e o `.htaccess` bloqueia os dois).
4. Confirmar com o cliente: número da Rua Quatá (o site antigo diz "1"; o BaresSP diz 1016 para o Vitrinni Lounge),
   número da Rua Diana (Perdizes) e da Rua Professor Atílio Innocenti (Espaço K). Corrigir em `tools/gerar.py` e rodar de novo.
5. Pedir acesso ao **Search Console** (ou criar a propriedade de domínio) e ao GA4, se existir. Hoje o site não tem nenhuma tag.

## Logo depois do lançamento

```bash
for u in / /listing/la-fiesta/ /listing/notizia/ /sobre/ /orcamento/ /home-static/ /cart/ /wp-sitemap.xml; do
  printf "%-28s " $u; curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" https://espacosvilaolimpia.com.br$u; done
curl -sI http://www.espacosvilaolimpia.com.br/ | grep -i location
```

Esperado: 200 nas páginas reais, 301 nas antigas, 410 em `/cart/`, 301 `http`/`www` → `https://espacosvilaolimpia.com.br/`.

No Search Console: enviar `/sitemap.xml`, remover o `wp-sitemap.xml`, pedir indexação da home e das 6 páginas `/listing/`,
e testar 2 páginas no Teste de pesquisa aprimorada (schema).

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

O WordPress fica intacto até a troca. Se algo der errado: restaurar o backup do passo 1 (ou voltar o DNS) e investigar com calma.

## Como editar

Todo o conteúdo está em `tools/gerar.py` (lista `SPACES`). Editou, rode `python3 tools/gerar.py` na pasta do site.
Não edite os `index.html` à mão: são sobrescritos.
