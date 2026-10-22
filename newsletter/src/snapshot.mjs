// Render newsletter/<slug>/index.html to a single tall PDF (and optionally a PNG).
//
//   node newsletter/src/snapshot.mjs <slug> <base_url> <pdf-name> [png-path]
//
// The HTML references images by their production URL (base_url/...), so those
// requests are served from the local newsletter/ folder instead; that lets the
// PDF be built before the images are deployed. Called by build.py --pdf.
import { createRequire } from "node:module";
import { readFile } from "node:fs/promises";
import { execSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
let playwright;
try {
  playwright = require("playwright");
} catch {
  const globalRoot = execSync("npm root -g").toString().trim();
  playwright = require(path.join(globalRoot, "playwright"));
}

const [slug, baseUrl, pdfName, pngPath] = process.argv.slice(2);
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const base = baseUrl.replace(/\/$/, "");
const TYPES = { ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".html": "text/html" };

const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
const browser = await playwright.chromium.launch(proxy ? { proxy: { server: proxy } } : {});
const page = await browser.newPage({ viewport: { width: 640, height: 1000 }, ignoreHTTPSErrors: true });

await page.route(`${base}/**`, async (route) => {
  const rel = decodeURIComponent(new URL(route.request().url()).pathname)
    .replace(new URL(base).pathname, "")
    .replace(/\/$/, "/index.html");
  const file = path.join(ROOT, rel);
  try {
    route.fulfill({ body: await readFile(file), contentType: TYPES[path.extname(file)] || "application/octet-stream" });
  } catch {
    route.fulfill({ status: 404, body: "missing: " + rel });
  }
});

await page.goto(`${base}/${slug}/`, { waitUntil: "networkidle" });
await page.evaluate(() => document.fonts.ready);
const height = await page.evaluate(() => document.documentElement.scrollHeight);

const pdfPath = path.join(ROOT, slug, pdfName);
await page.pdf({ path: pdfPath, width: "640px", height: `${height + 2}px`, printBackground: true, pageRanges: "1" });
console.log(`wrote ${path.relative(path.dirname(ROOT), pdfPath)}`);
if (pngPath) {
  await page.screenshot({ path: pngPath, fullPage: true });
  console.log(`wrote ${pngPath}`);
}
await browser.close();
