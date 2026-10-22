#!/usr/bin/env python3
"""
Build the GUAC Network Brief (franchise-partner newsletter) from JSON.

    python3 newsletter/src/build.py                 # build every issue + archive
    python3 newsletter/src/build.py 2026-10         # build one issue
    python3 newsletter/src/build.py 2026-10 --pdf   # ...and its PDF + PNG preview

Content lives in newsletter/src/issues/<YYYY-MM>.json, shared settings in
newsletter/src/config.json. Output per issue, both email-safe (tables +
inline styles):
  newsletter/<YYYY-MM>/index.html  web version, relative image paths
  newsletter/<YYYY-MM>/email.html  paste into the email platform, absolute URLs

Standard library only. See newsletter/src/README.md for the section types.
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent  # newsletter/
ISSUES = SRC / "issues"

# ---------------------------------------------------------------- design tokens
DARK = "#181716"
CREAM = "#eee2bb"
SAGE = "#b8c19a"
SAND = "#e2ddc6"
LIGHT_INK = "#ebe4cb"  # text on DARK
KICKER = "#a3b07e"  # sage text on CREAM
PAGE_BG = "#f3f0e6"
WIDTH = 600

FONT = "'Jost','Futura','Futura PT','Century Gothic','Trebuchet MS',Arial,sans-serif"

THEMES = {
    "sand": (SAND, DARK),
    "sage": (SAGE, DARK),
    "cream": (CREAM, DARK),
    "dark": (DARK, LIGHT_INK),
    "white": ("#ffffff", DARK),
}



class Ctx:
    """Per-issue build context: resolves URLs and holds the current text colour."""

    def __init__(self, config, issue, slug, email=False):
        self.config = config
        self.issue = issue
        self.slug = slug
        self.email = email
        # Email copies need absolute URLs; the web copy uses relative ones so it
        # also works on Pages previews and when opened from disk.
        self.base = config["base_url"].rstrip("/")
        self.issue_url = f"{self.base}/{slug}/" if email else ""
        self.fg = DARK

    def asset(self, src):
        if re.match(r"^https?://", src):
            return src
        if src.startswith("shared/"):
            return f"{self.base}/{src}" if self.email else f"../{src}"
        return self.issue_url + src

    def href(self, ref):
        if ref == "@pdf":
            return self.issue_url + pdf_name(self.slug)
        if ref == "@web":
            return f"{self.base}/{self.slug}/"
        if ref.startswith("@"):
            return self.config["links"][ref[1:]]
        return ref


def pdf_name(slug):
    return f"guac-network-brief-{slug}.pdf"


# ---------------------------------------------------------------- text helpers
def fmt(text, ctx, link_colour=None):
    """Fill {month}/{year}/{issue}, escape, then apply **bold**, [label](url) and newlines -> <br>."""
    for key in ("month", "year", "issue"):
        text = text.replace("{" + key + "}", str(ctx.issue[key]))
    out = html.escape(text, quote=False)
    out = re.sub(r"\*\*(.+?)\*\*", r'<strong style="font-weight:700;">\1</strong>', out)
    colour = link_colour or ctx.fg

    def link(m):
        url = html.escape(ctx.href(html.unescape(m.group(2))))
        return f'<a href="{url}" style="color:{colour};text-decoration:underline;">{m.group(1)}</a>'

    out = re.sub(r"\[(.+?)\]\((.+?)\)", link, out)
    return out.replace("\n", "<br>")


def style(**kw):
    return ";".join(f"{k.replace('_', '-')}:{v}" for k, v in kw.items()) + ";"


def text_style(size, weight=400, colour=None, lh=1.45, extra=""):
    return style(font_family=FONT, font_size=f"{size}px", font_weight=weight,
                 line_height=lh, color=colour or DARK, margin=0) + extra


def row(inner, bg, pad="0", cls=""):
    """One full-width band of the email."""
    c = f' class="{cls}"' if cls else ""
    return (f'<tr><td{c} bgcolor="{bg}" style="background-color:{bg};padding:{pad};">'
            f"{inner}</td></tr>\n")


def table(inner, width="100%", extra=""):
    return (f'<table role="presentation" width="{width}" cellpadding="0" cellspacing="0" '
            f'border="0" style="border-collapse:collapse;{extra}">{inner}</table>')


def button(text, href, ctx, bg=DARK, fg=LIGHT_INK, size=17, full=False, upper=True):
    width = ' width="100%"' if full else ""
    return (
        f'<table role="presentation" cellpadding="0" cellspacing="0" border="0"{width} '
        f'style="border-collapse:separate;margin:8px 0 18px;"><tr>'
        f'<td align="center" bgcolor="{bg}" style="border-radius:16px;background-color:{bg};">'
        f'<a href="{html.escape(ctx.href(href))}" style="{text_style(size, 700, fg, 1.2)}'
        f'display:block;padding:15px 22px;text-decoration:none;border-radius:16px;'
        f'{"text-transform:uppercase;" if upper else ""}letter-spacing:.02em;">{fmt(text, ctx, fg)}</a>'
        f"</td></tr></table>"
    )


def heading(text, ctx, size=44, colour=None, upper=False, pad="0 0 22px"):
    tt = "text-transform:uppercase;" if upper else ""
    return (f'<h2 style="{text_style(size, 700, colour or ctx.fg, 1.0)}padding:{pad};'
            f'letter-spacing:-.01em;{tt}">{fmt(text, ctx)}</h2>')


def bullet_rows(items, ctx, size=15, marker="&#9679;", gap=12, marker_w=26):
    rows = "".join(
        f'<tr><td valign="top" width="{marker_w}" style="{text_style(size, 400, ctx.fg)}'
        f'font-size:{size - 6}px;line-height:{size * 1.45}px;padding:0 0 {gap}px;">{marker}</td>'
        f'<td valign="top" style="{text_style(size, 400, ctx.fg)}padding:0 0 {gap}px;">'
        f"{fmt(item, ctx)}</td></tr>"
        for item in items
    )
    return table(rows)


# ---------------------------------------------------------------- panel blocks
def block_subhead(b, ctx):
    return (f'<p style="{text_style(16, 700, ctx.fg, 1.3)}text-transform:uppercase;'
            f'padding:6px 0 10px;">{fmt(b["text"], ctx)}</p>')


def block_p(b, ctx):
    return f'<p style="{text_style(15, 400, ctx.fg, 1.5)}padding:0 0 14px;">{fmt(b["text"], ctx)}</p>'


def block_bullets(b, ctx):
    return f'<div style="padding:0 0 10px;">{bullet_rows(b["items"], ctx, gap=4, marker_w=18)}</div>'


def block_lines(b, ctx):
    return "".join(
        f'<p style="{text_style(16, 700, ctx.fg, 1.4)}padding:0 0 4px;">{fmt(t, ctx)}</p>'
        for t in b["items"]
    ) + '<div style="height:10px;line-height:10px;font-size:0;">&nbsp;</div>'


def block_numbered(b, ctx):
    compact = b.get("compact")
    out = []
    for i, item in enumerate(b["items"], 1):
        tsize = 17 if compact else 21
        parts = [
            table(
                f'<tr><td valign="top" width="{30 if compact else 40}" '
                f'style="{text_style(tsize, 700, ctx.fg, 1.2)}">{i}.</td>'
                f'<td valign="top" style="{text_style(tsize, 700, ctx.fg, 1.2)}">'
                f'{fmt(item["title"], ctx)}</td></tr>'
            )
        ]
        indent = 30 if compact else 40
        if item.get("text"):
            parts.append(f'<p style="{text_style(15, 400, ctx.fg, 1.45)}padding:{4 if compact else 10}px 0 0 {indent}px;">'
                         f'{fmt(item["text"], ctx)}</p>')
        if item.get("bullets"):
            parts.append(f'<div style="padding:12px 0 0 {indent - 26 if indent > 26 else 0}px;">'
                         f'{bullet_rows(item["bullets"], ctx)}</div>')
        out.append(f'<div style="padding:0 0 {10 if compact else 16}px;">{"".join(parts)}</div>')
    return "".join(out)


def block_button(b, ctx):
    return button(b["text"], b["href"], ctx)


def block_images(b, ctx):
    items = b["items"]
    gap = 12
    cells = []
    for i, im in enumerate(items):
        img = (f'<img src="{html.escape(ctx.asset(im["src"]))}" alt="{html.escape(im.get("alt", ""))}" '
               f'width="100%" style="display:block;width:100%;height:auto;border:0;">')
        href = im.get("href") or b.get("href")
        if href:
            img = f'<a href="{html.escape(ctx.href(href))}">{img}</a>'
        pad = f"0 {gap // 2 if i < len(items) - 1 else 0}px 0 {gap // 2 if i else 0}px"
        cells.append(f'<td valign="top" width="{100 // len(items)}%" style="padding:{pad};">{img}</td>')
    return f'<div style="padding:4px 0 22px;">{table("<tr>" + "".join(cells) + "</tr>")}</div>'


def block_tagged(b, ctx):
    """Black label box on the left, content on the right (stacks on mobile)."""
    tag = (f'<table role="presentation" width="96" cellpadding="0" cellspacing="0" border="0" '
           f'style="border-collapse:collapse;"><tr><td align="center" valign="middle" height="96" '
           f'bgcolor="{DARK}" style="background-color:{DARK};padding:8px 6px;'
           f'{text_style(12, 700, LIGHT_INK, 1.15)}text-transform:uppercase;">'
           f'{fmt(b["tag"], ctx, LIGHT_INK)}</td></tr></table>')
    body = render_blocks(b["blocks"], ctx)
    return table(
        f'<tr><td class="stack stack-gap" valign="top" width="96" style="padding:0 18px 0 0;">{tag}</td>'
        f'<td class="stack" valign="top" style="padding:0;">{body}</td></tr>',
        extra="margin:0 0 18px;",
    )


BLOCKS = {
    "subhead": block_subhead,
    "p": block_p,
    "bullets": block_bullets,
    "lines": block_lines,
    "numbered": block_numbered,
    "button": block_button,
    "images": block_images,
    "tagged": block_tagged,
}


def render_blocks(blocks, ctx):
    out = []
    for b in blocks:
        if b["type"] not in BLOCKS:
            sys.exit(f"Unknown block type: {b['type']!r}")
        out.append(BLOCKS[b["type"]](b, ctx))
    return "".join(out)


# ---------------------------------------------------------------- sections
def sec_masthead(s, ctx):
    issue = ctx.issue
    inner = (
        f'<p style="{text_style(13, 500, LIGHT_INK, 1)}letter-spacing:.3em;text-align:right;'
        f'padding:0 92px 6px 0;" class="mast-issue">ISSUE {issue["issue"]}</p>'
        f'<img src="{ctx.asset("shared/wordmark-cream.png")}" width="300" alt="GUAC" '
        f'style="display:block;margin:0 auto;width:300px;max-width:70%;height:auto;border:0;">'
        f'<p style="{text_style(19, 400, LIGHT_INK, 1)}letter-spacing:.42em;text-align:center;'
        f'padding:14px 0 0 .42em;">NETWORK BRIEF</p>'
    )
    return row(inner, DARK, "34px 24px 30px")


def sec_headline(s, ctx):
    inner = (
        f'<p style="{text_style(40, 400, KICKER, 1.05)}text-align:center;text-transform:uppercase;">'
        f'{fmt(s["kicker"], ctx)}</p>'
        f'<p style="{text_style(62, 800, DARK, 1.05)}text-align:center;text-transform:uppercase;'
        f'letter-spacing:.01em;" class="hl-title">{fmt(s["title"], ctx)}</p>'
    )
    return row(inner, s.get("bg", CREAM), "24px 20px 24px")


def sec_image(s, ctx):
    img = (f'<img src="{html.escape(ctx.asset(s["src"]))}" width="{WIDTH}" alt="{html.escape(s.get("alt", ""))}" '
           f'style="display:block;width:100%;height:auto;border:0;">')
    if s.get("href"):
        img = f'<a href="{html.escape(ctx.href(s["href"]))}">{img}</a>'
    return row(img, s.get("bg", DARK))


def sec_letter(s, ctx):
    bg, ctx.fg = THEMES[s.get("theme", "sage")]
    paras = "".join(f'<p style="{text_style(16, 400, ctx.fg, 1.55)}padding:0 0 18px;">{fmt(p, ctx)}</p>'
                    for p in s["paragraphs"])
    sig = table(
        f'<tr><td class="stack stack-center stack-gap" width="190" valign="middle" style="padding:0 24px 0 50px;">'
        f'<img src="{html.escape(ctx.asset(s["photo"]))}" width="180" alt="{html.escape(s["name"])}" '
        f'style="display:block;width:180px;height:180px;border:0;border-radius:50%;margin:0 auto;"></td>'
        f'<td class="stack stack-center" valign="middle" style="{text_style(20, 400, ctx.fg, 1.3)}">'
        f'{fmt(s.get("signoff", "Sincerely,"), ctx)}<br><strong style="font-weight:700;">{fmt(s["name"], ctx)}</strong>'
        f"</td></tr>"
    )
    inner = (heading(s["heading"], ctx, 46, pad="0 0 26px")
             + f'<p style="{text_style(16, 400, ctx.fg, 1.55)}padding:0 0 18px;">{fmt(s["salutation"], ctx)}</p>'
             + paras + f'<div style="padding:22px 0 0;">{sig}</div>')
    return row(inner, bg, "52px 46px 46px", "pad")


def sec_panel(s, ctx):
    bg, ctx.fg = THEMES[s.get("theme", "sand")]
    inner = (heading(s["heading"], ctx, 46, pad="0 0 28px") if s.get("heading") else "") + render_blocks(s["blocks"], ctx)
    if s.get("inset"):
        outer = s.get("outer", "#ffffff")
        inner = table(f'<tr><td class="pad" bgcolor="{bg}" style="background-color:{bg};padding:46px 34px 26px;">'
                      f"{inner}</td></tr>")
        return row(inner, outer, "24px 22px", "inset")
    return row(inner, bg, "46px 34px 26px", "pad")


def sec_spotlight(s, ctx):
    bg, ctx.fg = THEMES[s.get("theme", "dark")]
    out = [heading(s["heading"], ctx, 44, upper=True, pad="0 0 34px")]
    for store in s["stores"]:
        reviews = "".join(
            f'<p style="{text_style(17, 700, ctx.fg, 1.3)}padding:0 0 2px;">{fmt(r["author"], ctx)}</p>'
            f'<p style="{text_style(16, 400, ctx.fg, 1.45)}padding:0 0 16px;">&ldquo;{fmt(r["text"], ctx)}&rdquo;</p>'
            for r in store.get("reviews", [])
        )
        if reviews:
            reviews = (f'<p style="{text_style(17, 700, ctx.fg, 1.3)}text-transform:uppercase;padding:6px 0 14px;">'
                       f'{fmt(s.get("reviews_label", "Google Reviews"), ctx)}</p>' + reviews)
        body = f'<p style="{text_style(16, 400, ctx.fg, 1.5)}padding:0 0 16px;">{fmt(store["story"], ctx)}</p>' + reviews
        photo = (f'<img src="{html.escape(ctx.asset(store["photo"]))}" width="150" alt="{html.escape(store["name"])} storefront" '
                 f'style="display:block;width:150px;height:150px;border:0;border-radius:50%;">') if store.get("photo") else ""
        out.append(
            f'<h3 style="{text_style(34, 700, ctx.fg, 1.1)}padding:0 0 22px;">{fmt(store["name"], ctx)}</h3>'
            + table(f'<tr><td class="stack stack-gap" valign="top" width="150" style="padding:0 26px 0 0;">{photo}</td>'
                    f'<td class="stack" valign="top">{body}</td></tr>', extra="margin:0 0 26px;")
        )
    return row("".join(out), bg, "46px 34px 30px", "pad")


def sec_promo(s, ctx):
    ctx.fg = DARK
    steps = "".join(
        f'<tr><td valign="top" width="24" style="{text_style(16, 400)}padding:0 0 14px;">{i}.</td>'
        f'<td valign="top" style="{text_style(16, 400)}padding:0 0 14px;">{fmt(t, ctx)}</td></tr>'
        for i, t in enumerate(s["steps"], 1)
    )
    card = (
        f'<p class="promo-title" style="{text_style(54, 900, DARK, .95)}text-align:center;text-transform:uppercase;'
        f'padding:34px 16px 16px;letter-spacing:.01em;">{fmt(s["title"], ctx)}</p>'
        + table(f'<tr><td align="center" bgcolor="{DARK}" style="background-color:{DARK};padding:9px 12px;'
                f'{text_style(19, 700, LIGHT_INK, 1.1)}text-transform:uppercase;">{fmt(s["tag"], ctx, LIGHT_INK)}</td></tr>',
                width="70%", extra="margin:0 auto 22px;")
        + (f'<img src="{html.escape(ctx.asset(s["image"]))}" width="552" alt="{html.escape(s.get("image_alt", ""))}" '
           f'style="display:block;width:100%;height:auto;border:0;">' if s.get("image") else "")
        + f'<p style="{text_style(25, 400, DARK, 1.15)}text-align:center;text-transform:uppercase;padding:26px 20px 22px;">'
          f'{fmt(s["subtitle"], ctx)}</p>'
        + f'<div style="padding:0 60px;" class="promo-steps">{table(steps)}</div>'
        + (f'<p style="{text_style(17, 700, DARK, 1.3)}text-align:center;text-transform:uppercase;padding:18px 24px 4px;">'
           f'{fmt(s["line_label"], ctx)}</p>'
           f'<p style="{text_style(16, 400, DARK, 1.4)}text-align:center;padding:0 24px 34px;">{fmt(s["line"], ctx)}</p>'
           if s.get("line") else '<div style="height:26px;"></div>')
    )
    card = table(f'<tr><td bgcolor="#ffffff" style="background-color:#ffffff;box-shadow:4px 4px 6px rgba(0,0,0,.35);">'
                 f"{card}</td></tr>")
    return row(card, THEMES[s.get("theme", "sand")][0], "40px 24px 44px", "inset")


def sec_button(s, ctx):
    return row(button(s["text"], s["href"], ctx, size=24, full=True, upper=s.get("uppercase", False)),
               s.get("bg", "#ffffff"), "26px 40px 22px", "inset")


def sec_footer(s, ctx):
    cfg = ctx.config
    foot = cfg["footer"]
    rule = f'<div style="height:1px;line-height:1px;font-size:0;background-color:{DARK};">&nbsp;</div>'
    icons = "".join(
        f'<td style="padding:0 16px;"><a href="{html.escape(cfg["links"][n])}">'
        f'<img src="{ctx.asset(f"shared/icon-{n}-dark.png")}" width="40" height="40" alt="{n.title()}" '
        f'style="display:block;width:40px;height:40px;border:0;"></a></td>'
        for n in foot["social"]
    )
    inner = (
        f'<a href="{html.escape(cfg["links"]["website"])}"><img src="{ctx.asset("shared/logo-dark.png")}" width="300" '
        f'alt="GUAC Mexi Grill" style="display:block;margin:0 auto 26px;width:300px;max-width:70%;height:auto;border:0;"></a>'
        + rule
        + f'<div style="padding:18px 0;">{table("<tr>" + icons + "</tr>", width="auto", extra="margin:0 auto;")}</div>'
        + rule
        + f'<p style="{text_style(15, 400, DARK, 1.6)}text-align:center;padding:24px 0 0;">{fmt(foot["address"], ctx)}<br>'
          f'<a href="{html.escape(cfg["links"]["website"])}" style="color:{DARK};text-decoration:none;">'
          f'{html.escape(foot["website_label"])}</a></p>'
    )
    return row(inner, SAND, "44px 50px 40px", "pad")


SECTIONS = {
    "masthead": sec_masthead,
    "headline": sec_headline,
    "image": sec_image,
    "letter": sec_letter,
    "panel": sec_panel,
    "spotlight": sec_spotlight,
    "promo": sec_promo,
    "button": sec_button,
    "footer": sec_footer,
}

# ---------------------------------------------------------------- page
HEAD_CSS = f"""
  body {{ margin:0; padding:0; background-color:{PAGE_BG}; -webkit-text-size-adjust:100%; }}
  img {{ -ms-interpolation-mode:bicubic; }}
  a {{ text-decoration:underline; }}
  @media only screen and (max-width:620px) {{
    .wrap {{ width:100% !important; }}
    .pad {{ padding-left:22px !important; padding-right:22px !important; }}
    .inset {{ padding-left:10px !important; padding-right:10px !important; }}
    .stack {{ display:block !important; width:100% !important; padding-right:0 !important; padding-left:0 !important; }}
    .stack-gap {{ padding-bottom:16px !important; }}
    .stack-center {{ text-align:center !important; }}
    .stack-center img {{ margin:0 auto !important; }}
    .hl-title {{ font-size:46px !important; }}
    .promo-title {{ font-size:38px !important; }}
    .promo-steps {{ padding:0 22px !important; }}
    .mast-issue {{ padding-right:12px !important; }}
  }}
"""


def render_issue(config, issue, slug, email=False):
    ctx = Ctx(config, issue, slug, email)
    body = []
    for s in issue["sections"]:
        if s["type"] not in SECTIONS:
            sys.exit(f"{slug}: unknown section type {s['type']!r}")
        ctx.fg = DARK
        body.append(SECTIONS[s["type"]](s, ctx))

    title = f'{config["title"]} — {issue["month"]} {issue["year"]}'
    web_link = (f'<a href="{ctx.href("@web")}" style="color:#6b675c;">View in browser</a> &nbsp;&middot;&nbsp;\n'
                if email else "")
    pre = html.escape(issue.get("preheader", ""))
    return f"""<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="robots" content="noindex, nofollow">
<meta name="x-apple-disable-message-reformatting">
<title>{html.escape(issue.get("subject", title))}</title>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<style>{HEAD_CSS}</style>
</head>
<body style="margin:0;padding:0;background-color:{PAGE_BG};">
<!-- Generated by newsletter/src/build.py from issues/{slug}.json. Edit the JSON, not this file. -->
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">{pre}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{PAGE_BG}" style="background-color:{PAGE_BG};">
<tr><td align="center" style="padding:0;">
<p style="{text_style(12, 400, '#6b675c', 1.4)}text-align:center;padding:12px 10px;">
{web_link}<a href="{ctx.href('@pdf')}" style="color:#6b675c;">Download PDF</a></p>
<table role="presentation" class="wrap" width="{WIDTH}" cellpadding="0" cellspacing="0" border="0" bgcolor="#ffffff" style="border-collapse:collapse;width:{WIDTH}px;max-width:100%;background-color:#ffffff;">
{"".join(body)}</table>
<div style="height:24px;line-height:24px;font-size:0;">&nbsp;</div>
</td></tr></table>
</body>
</html>
"""


def render_archive(config, issues):
    rows = "".join(
        f'<li style="margin:0 0 10px;"><a href="{slug}/" style="color:{DARK};">'
        f'Issue {iss["issue"]} — {iss["month"]} {iss["year"]}</a> &nbsp;·&nbsp; '
        f'<a href="{slug}/{pdf_name(slug)}" style="color:#6b675c;">PDF</a></li>'
        for slug, iss in sorted(issues, reverse=True)
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{html.escape(config["title"])} — Archive</title>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;700&display=swap" rel="stylesheet">
</head>
<body style="margin:0;background:{SAND};font-family:{FONT};color:{DARK};">
<!-- Generated by newsletter/src/build.py. -->
<main style="max-width:600px;margin:0 auto;padding:48px 22px;">
<img src="shared/logo-dark.png" width="220" alt="GUAC Mexi Grill" style="display:block;margin:0 0 28px;">
<h1 style="font-size:34px;margin:0 0 24px;">{html.escape(config["title"])}</h1>
<ul style="list-style:none;padding:0;margin:0;font-size:18px;">{rows}</ul>
</main>
</body>
</html>
"""


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main(argv):
    want_pdf = "--pdf" in argv
    slugs = [a for a in argv if not a.startswith("--")]
    config = load(SRC / "config.json")
    all_issues = []
    for path in sorted(ISSUES.glob("*.json")):
        slug = path.stem
        if not re.fullmatch(r"\d{4}-\d{2}", slug):
            sys.exit(f"Issue files must be named YYYY-MM.json, got {path.name}")
        issue = load(path)
        all_issues.append((slug, issue))
        if slugs and slug not in slugs:
            continue
        (ROOT / slug).mkdir(parents=True, exist_ok=True)
        for name, email in (("index.html", False), ("email.html", True)):
            out = ROOT / slug / name
            out.write_text(render_issue(config, issue, slug, email), encoding="utf-8")
            print(f"wrote {out.relative_to(ROOT.parent)}")
        if want_pdf:
            subprocess.run(["node", str(SRC / "snapshot.mjs"), slug, config["base_url"], pdf_name(slug)], check=True)
    for s in slugs:
        if s not in dict(all_issues):
            sys.exit(f"No issue file: newsletter/src/issues/{s}.json")
    (ROOT / "index.html").write_text(render_archive(config, all_issues), encoding="utf-8")
    print("wrote newsletter/index.html")


if __name__ == "__main__":
    main(sys.argv[1:])
