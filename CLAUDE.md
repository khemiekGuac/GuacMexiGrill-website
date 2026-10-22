# GUAC Mexi Grill websites

Two static sites in one repo, each deployed by its own Cloudflare Pages project:

| Site | Pages project | Source root |
|---|---|---|
| guacmexigrill.ca | `guacmexigrill-website` | repo root (everything outside `com-site/`) |
| guacmexigrillusa.com | `guacmexigrillusawebsite` | `com-site/` |

- No build step. Pages Functions live in `functions/` (.ca) and `com-site/functions/` (US).
- Each site's `functions/_middleware.js` 301-redirects `www.*` to the bare domain and
  404s internal files (`*.md`, `*.py`, `*.json(c)`, dotfiles, `/functions/`, and
  `/com-site/` on .ca). Keep new internal files covered by that blocklist.
- Canonical, `og:url`, hreflang and JSON-LD URLs use extensionless paths
  (`https://guacmexigrill.ca/about`), because Cloudflare 308-redirects `*.html`.
- Each site has its own `sitemap.xml` and `robots.txt`. Add new pages to the sitemap
  and bump `<lastmod>` when a page changes meaningfully.

## Location status

Locations are cards in `locations.html`; the loyalty sign-up store list is in `loyalty.html`.

- **Temporarily closed:** card gets `loc-card--closed`, a
  `<div class="loc-status--closed">Temporarily Closed</div>` badge and a closure note in
  `loc-hours`. In `loyalty.html` the option becomes `<option disabled>City (Temporarily Closed)</option>`.
- **Permanently closed:** card gets `loc-card--closed`, a `Permanently Closed` badge,
  address only (no phone, directions or gift-card links) and `loc-hours` reading
  "Permanently closed". The option is removed from `loyalty.html`.
- Province tab counts include closed cards.

| Location | Status |
|---|---|
| Red Deer, AB (GMG039) | Permanently closed |
| Winnipeg, MB (GMG041) — 584 Pembina Hwy | Permanently closed (closed in 2025) |
| Edmonton — Harvest Hill, AB | Temporarily closed |
| Grande Prairie, AB | Temporarily closed |
| Moose Jaw, SK | Temporarily closed |

## Location count

The public "56+" count lives in `site-config.js` (`SITE.locationCount`, drives
`data-loc-count` elements) and is also hard-coded in page titles, meta/OG/Twitter
descriptions, JSON-LD and body copy. Update all of them together.

## Newsletter (GUAC Network Brief)

Monthly franchise-partner newsletter in `newsletter/`, documented in `newsletter/README.md`.
It is NOT hosted on the site: the middleware 404s all of `/newsletter/`. Content is
`newsletter/issues/YYYY-MM.json`, photos `newsletter/images/YYYY-MM/`; run
`python3 newsletter/build.py YYYY-MM --pdf` to regenerate `newsletter/output/YYYY-MM.html`
(self-contained, images embedded) and its PDF — never hand-edit those.
