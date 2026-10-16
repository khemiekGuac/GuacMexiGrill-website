/**
 * Pages middleware for guacmexigrillusa.com — runs on every request.
 *
 * This project's root is /com-site, so internal files that live in it
 * (README, Pages Functions source, dotfiles) would otherwise be served
 * publicly. They are answered with a 404.
 *
 * www.* is permanently redirected (301) to the bare domain so search engines
 * see one copy of each page.
 */

// Files in the repo that must never be served publicly.
const BLOCKED_PATH =
  /^\/(functions(\/|$)|\.(?!well-known\/)|[^/]*\.(py|md|jsonc?|toml)$)/i;

export async function onRequest(context) {
  const host = (context.request.headers.get("host") || "").toLowerCase();
  if (host.startsWith("www.")) {
    const url = new URL(context.request.url);
    url.hostname = host.slice(4);
    url.protocol = "https:";
    return Response.redirect(url.toString(), 301);
  }

  let path = new URL(context.request.url).pathname;
  try {
    path = decodeURIComponent(path);
  } catch (e) {
    // Malformed escapes: test the raw path.
  }

  if (BLOCKED_PATH.test(path)) {
    return new Response("Not found", {
      status: 404,
      headers: {
        "content-type": "text/plain; charset=utf-8",
        "x-robots-tag": "noindex, nofollow",
        "cache-control": "no-store",
      },
    });
  }

  return context.next();
}
