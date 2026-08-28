/**
 * Root Pages middleware — runs on every request to the .ca site.
 *
 * Purpose: keep non-production hostnames out of search engines with a
 * server-side `X-Robots-Tag: noindex` header. The pre-existing inline
 * <meta name="robots"> snippet is client-side JS, which crawlers frequently
 * ignore — that is why staging.guacmexigrill.ca got indexed. An HTTP response
 * header is honoured reliably and applies to every response type (HTML, JSON,
 * assets), not just rendered pages.
 *
 * Production hostnames are passed through untouched. Access is NOT blocked —
 * staging stays reachable by direct link for internal staff; it is only made
 * undiscoverable via search. (For true access control, put staging behind
 * Cloudflare Access in the dashboard.)
 */
export async function onRequest(context) {
  const response = await context.next();

  try {
    const host = (context.request.headers.get("host") || "").toLowerCase();
    const isNonProd = host.startsWith("staging.") || host.endsWith(".pages.dev");

    if (isNonProd) {
      const headers = new Headers(response.headers);
      headers.set("X-Robots-Tag", "noindex, nofollow");
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers,
      });
    }
  } catch (e) {
    // On any error, fall through and serve the unmodified response so a
    // safeguard bug can never take down production.
  }

  return response;
}
