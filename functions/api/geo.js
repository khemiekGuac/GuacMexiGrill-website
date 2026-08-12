export async function onRequest(context) {
  const country = context.request.cf?.country || "UNKNOWN";
  return new Response(JSON.stringify({ country }), {
    headers: {
      "content-type": "application/json",
      "cache-control": "no-store",
    },
  });
}
