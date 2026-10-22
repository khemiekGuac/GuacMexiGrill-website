// Render a built newsletter HTML file to a single tall PDF.
//
//   node newsletter/snapshot.mjs <html-path> <pdf-path> [png-path]
//
// Called by build.py --pdf. Needs Node + Playwright (Chromium).
import { createRequire } from "node:module";
import { execSync } from "node:child_process";
import path from "node:path";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
let playwright;
try {
  playwright = require("playwright");
} catch {
  playwright = require(path.join(execSync("npm root -g").toString().trim(), "playwright"));
}

const [htmlPath, pdfPath, pngPath] = process.argv.slice(2);
const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
const browser = await playwright.chromium.launch(proxy ? { proxy: { server: proxy } } : {});
const page = await browser.newPage({ viewport: { width: 640, height: 1000 }, ignoreHTTPSErrors: true });

await page.goto(pathToFileURL(path.resolve(htmlPath)).href, { waitUntil: "networkidle" });
await page.evaluate(() => document.fonts.ready);
const height = await page.evaluate(() => document.documentElement.scrollHeight);

await page.pdf({ path: pdfPath, width: "640px", height: `${height + 2}px`, printBackground: true, pageRanges: "1" });
console.log(`wrote ${path.relative(process.cwd(), pdfPath)}`);
if (pngPath) {
  await page.screenshot({ path: pngPath, fullPage: true });
  console.log(`wrote ${pngPath}`);
}
await browser.close();
