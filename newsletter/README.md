# GUAC Network Brief — monthly newsletter

Franchise-partner newsletter, built from JSON into one email-safe HTML file.

```
newsletter/                 (whole folder is 404'd on the website — never hosted)
  build.py                    generator (Python 3, stdlib only)
  snapshot.mjs                HTML → PDF via Playwright (used by --pdf)
  config.json                 links, footer, optional image_base_url
  issues/YYYY-MM.json         one file per issue: all the words
  images/shared/              logos + social icons used by every issue
  images/YYYY-MM/             this issue's photos
  output/YYYY-MM.html         GENERATED — the newsletter, images embedded
  output/YYYY-MM.pdf          GENERATED with --pdf
```

## Monthly update

1. Copy last month's issue: `cp issues/2026-10.json issues/2026-11.json`
2. Edit the copy: bump `issue`, `month`, `year`, `subject`, `preheader`, then
   rewrite the sections. Put new photos in `images/2026-11/` and refer to them
   by file name (`"photo": "store-alliston.png"`). Reusing an older photo:
   `"src": "../2026-10/hero.jpg"`.
3. Build: `python3 newsletter/build.py 2026-11 --pdf`
4. Use `output/2026-11.html` — open it in a browser to review, then copy its code.

Never hand-edit the files in `output/` — edit the JSON and rebuild.

## Images and email clients

`output/YYYY-MM.html` embeds every image inside the file, so it is fully
self-contained: it looks right opened in a browser, attached, or pasted into
most editors. Gmail and some other inboxes block embedded images, though. To
send it as an email to those, upload the `images/` folder to your email
platform (or any image host), set `image_base_url` in `config.json` to that
folder's URL, and rebuild — `output/YYYY-MM.hosted.html` then links to the
uploaded images instead (`<image_base_url>/2026-11/hero.jpg`,
`<image_base_url>/shared/logo-dark.png`).

The "download the newsletter" button only appears when the issue's `pdf_url`
is set (e.g. a shared-drive link to the PDF).

## Writing text

- `**bold**`, `[label](https://url)` and `\n` (line break) work in any text field.
- `{month}`, `{year}`, `{issue}` are filled in from the issue file.
- Link values starting with `@` come from `config.json` → `links`
  (`@linkedin`, `@media_kit`, …). `@pdf` = the issue's `pdf_url`.

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
