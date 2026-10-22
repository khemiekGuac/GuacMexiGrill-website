/**
 * Root Pages middleware — runs on every request.
 *
 * Two non-production behaviours; production hostnames are untouched:
 *
 *  1. staging.*  — the public staging custom domain is RETIRED. Every request
 *     is answered with `410 Gone` (plus a noindex header) so search engines
 *     drop the URL fast and visitors get an unambiguous "this no longer
 *     exists" signal. Internal staff use the project's *.pages.dev URL below.
 *
 *  2. *.pages.dev — Cloudflare preview URLs stay reachable for staff but are
 *     kept out of search with an `X-Robots-Tag: noindex` response header.
 *
 *  3. Internal repo files (scripts, config, docs, the US site's source under
 *     /com-site, the newsletter generator under /newsletter) are deployed
 *     alongside the site because the Pages project serves the repo root. They are answered with a 404 on every host.
 *
 *  4. www.*  — permanently redirected (301) to the bare domain so search
 *     engines see one copy of each page.
 *
 * NOTE: this only affects the staging domain if that domain is served by a
 * deployment built from this repository. If staging is a separate/stale
 * Cloudflare project, the custom domain + DNS record must be removed in the
 * dashboard for the URL to actually go away.
 */
// Files in the repo that must never be served publicly.
const BLOCKED_PATH =
  /^\/(com-site(\/|$)|functions(\/|$)|newsletter(\/|$)|\.(?!well-known\/)|[^/]*\.(py|md|jsonc?|toml)$)/i;

export async function onRequest(context) {
  const host = (context.request.headers.get("host") || "").toLowerCase();
  let path = new URL(context.request.url).pathname;
  try {
    path = decodeURIComponent(path);
  } catch (e) {
    // Malformed escapes: test the raw path.
  }

  // 4. Send www.* to the bare domain (one canonical host).
  if (host.startsWith("www.")) {
    const url = new URL(context.request.url);
    url.hostname = host.slice(4);
    url.protocol = "https:";
    return Response.redirect(url.toString(), 301);
  }

  // 3. Block internal repo files.
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

  // 1. Retire the public staging custom domain.
  if (host.startsWith("staging.")) {
    return new Response("This staging site has been retired.", {
      status: 410,
      headers: {
        "content-type": "text/plain; charset=utf-8",
        "x-robots-tag": "noindex, nofollow",
        "cache-control": "no-store",
      },
    });
  }

  const response = await context.next();

  // 2. Keep *.pages.dev previews out of search (still reachable for staff).
  try {
    if (host.endsWith(".pages.dev")) {
      const headers = new Headers(response.headers);
      headers.set("X-Robots-Tag", "noindex, nofollow");
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers,
      });
    }
  } catch (e) {
    // Fail open: never let the safeguard take down a response.
  }

  return response;
}
