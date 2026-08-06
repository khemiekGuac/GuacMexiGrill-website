/*
 * Single source of truth for site-wide values that appear as visible copy.
 *
 * To change the public location count everywhere it is displayed as body copy,
 * update SITE.locationCount below. Every element tagged with the
 * `data-loc-count` attribute will be set to this value on load.
 *
 * NOTE: SEO <title>, <meta description/og/twitter>, and JSON-LD values are
 * rendered at crawl time and cannot be driven from this runtime constant on a
 * build-less static site. Those still contain the literal count and must be
 * updated together with this value until a build step is introduced.
 */
window.SITE = window.SITE || {};
window.SITE.locationCount = "56+";

(function () {
  function apply() {
    document.querySelectorAll("[data-loc-count]").forEach(function (el) {
      el.textContent = window.SITE.locationCount;
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", apply);
  } else {
    apply();
  }
})();
