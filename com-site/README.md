# guacmexigrillusa.com — Cloudflare Pages project

This folder is the source root for the **guacmexigrillusa.com** site. It is a plain
multi-page static site (HTML + assets + one Pages Function), deployed as a **second,
independent Cloudflare Pages project** from the same Git repo as the `.ca` site.

## Pages (Part B)
- `index.html` — Home
- `about.html` — About Guac
- `franchising.html` — Franchising (application flow, investment, multi-unit table, OR/RI logic)
- `locations.html` — Locations (coming-soon only, no address list / map / email capture)
- `contact.html` — Contact (routes to the shared inbox, `info@guacmexigrill.ca`)
- `privacy.html` — Privacy Policy (Guacmexigrill Franchising LLC; US-facing)
- `terms.html` — Terms of Use (no governing-law clause, per spec B7)

## Geo banner (Part C)
- `functions/api/geo.js` — Pages Function that returns the visitor country (`GET /api/geo`).
- `assets/js/geo-banner.js` — client script, included on every page. On the `.com` site it
  triggers for **CA** visitors and points them to guacmexigrill.ca. (The `.ca` site carries the
  mirror-image script that triggers for **US** visitors and points to guacmexigrillusa.com.)

## Cloudflare setup — manual steps (dashboard, not automatable from the repo)
These require Cloudflare dashboard/API access and must be done by Khemie:

1. **Workers & Pages → Create → Pages → Connect to Git → this repo.**
2. **Root directory:** `/com-site`. **Build command:** none. **Build output directory:** `/`.
3. Deploy to the `*.pages.dev` preview URL first and confirm it renders.
4. **Custom domains:** attach `guacmexigrillusa.com` and `www.guacmexigrillusa.com` in this
   Pages project's settings — **only after** confirming the guacmexigrillusa.com Cloudflare zone
   shows **Active**. (See PR notes: zone-Active status could not be verified from the build
   environment.)
5. **Build watch paths** so a commit to one site doesn't rebuild the other:
   - `.com` project: `com-site/*`
   - `.ca` project: everything **outside** `com-site/*`.
6. Confirm SSL is active and that www/apex resolve consistently (one redirects to the other).

## Notes
- No gift card, LTO, allergen, or nutrition pages exist here by design.
- Entity throughout is **Guacmexigrill Franchising LLC** (never ATM Holdings Inc.).
- Images live in `com-site/images/` (this project's root cannot reach the repo-root `/images`).
