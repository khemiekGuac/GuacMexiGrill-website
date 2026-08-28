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
 * NOTE: this only affects the staging domain if that domain is served by a
 * deployment built from this repository. If staging is a separate/stale
 * Cloudflare project, the custom domain + DNS record must be removed in the
 * dashboard for the URL to actually go away.
 */
export async function onRequest(context) {
  const host = (context.request.headers.get("host") || "").toLowerCase();

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
