/**
 * Pages middleware for guacmexigrillusa.com — runs on every request.
 *
 * This project's root is /com-site, so internal files that live in it
 * (README, Pages Functions source, dotfiles) would otherwise be served
 * publicly. They are answered with a 404.
 */

// Files in the repo that must never be served publicly.
const BLOCKED_PATH =
  /^\/(functions(\/|$)|\.(?!well-known\/)|[^/]*\.(py|md|jsonc?|toml)$)/i;

export async function onRequest(context) {
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
