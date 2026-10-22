# GUAC Network Brief — monthly newsletter

Franchise-partner newsletter, built from JSON into one email-safe HTML file.

```
newsletter/
  src/                      ← source (404'd by functions/_middleware.js)
    build.py                  generator (Python 3, stdlib only)
    snapshot.mjs              HTML → PDF via Playwright (used by --pdf)
    config.json               links, footer, base URL — shared by every issue
    issues/YYYY-MM.json       one file per issue: all the words
  shared/                   logos + social icons used by every issue
  YYYY-MM/                  published issue (public URL, noindex)
    index.html                GENERATED — web version + email HTML
    guac-network-brief-YYYY-MM.pdf   GENERATED — the "download" PDF
    images/                   this issue's photos
  index.html                GENERATED — archive of all issues
```

Published at `https://guacmexigrill.ca/newsletter/YYYY-MM/` once merged.
`/newsletter/` is disallowed in robots.txt and every page is `noindex`.

## Monthly update

1. Copy last month's issue: `cp src/issues/2026-10.json src/issues/2026-11.json`
2. Edit the copy: bump `issue`, `month`, `year`, `subject`, `preheader`, then
   rewrite the sections. Put new photos in `newsletter/2026-11/images/`.
   Reusing an older photo: `"src": "../2026-10/images/hero.jpg"`.
3. Build: `python3 newsletter/src/build.py 2026-11 --pdf`
4. Open `newsletter/2026-11/index.html` to review, commit, merge → live.
5. Send: paste `newsletter/2026-11/index.html` into the email platform as
   custom HTML (images load from guacmexigrill.ca, so merge before sending).

Never hand-edit the generated `index.html` / PDF — edit the JSON and rebuild.

## Writing text

- `**bold**`, `[label](https://url)` and `\n` (line break) work in any text field.
- `{month}`, `{year}`, `{issue}` are filled in from the issue file.
- Link values starting with `@` come from `config.json` → `links`
  (`@linkedin`, `@media_kit`, …). `@pdf` = this issue's PDF, `@web` = its web page.

## Section types (`sections`, top to bottom)

| type | fields |
|---|---|
| `masthead` | — (GUAC / Network Brief / Issue N) |
| `headline` | `kicker` (small sage line), `title` (big black line) |
| `image` | `src`, `alt`, optional `href` |
| `letter` | `heading`, `salutation`, `paragraphs[]`, `signoff`, `name`, `photo` |
| `panel` | `heading`, `theme` (`sand`/`sage`/`cream`/`dark`/`white`), `inset` (white margin), `blocks[]` |
| `spotlight` | `heading`, `stores[]` → `name`, `photo`, `story`, `reviews[]` → `author`, `text` |
| `promo` | `title`, `tag`, `image`, `subtitle`, `steps[]`, `line_label`, `line` |
| `button` | `text`, `href`, optional `uppercase` |
| `footer` | — (from config.json) |

## Block types (inside a `panel` or a `tagged` block)

| type | fields |
|---|---|
| `subhead` | `text` (bold caps) |
| `p` | `text` |
| `bullets` | `items[]` |
| `lines` | `items[]` (bold one-liners) |
| `numbered` | `items[]` → `title`, optional `text`, optional `bullets[]`; `compact: true` for tight lists |
| `tagged` | `tag` (black label box on the left), `blocks[]` |
| `button` | `text`, `href` |
| `images` | `items[]` → `src`, `alt`; optional `href` (side by side) |

## Images

- Store photos: square-cropped circles, 300×300 PNG with transparency.
- Founder photo: 360×360 circle PNG. Full-width photos: ~930px wide JPG.
- Keep each issue's images under ~1.5 MB total; email clients load all of them.

## Requirements

Python 3 for the build. `--pdf` also needs Node + Playwright with Chromium.
