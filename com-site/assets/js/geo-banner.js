(function () {
  var CONFIG = {
    triggerCountry: "CA",
    triggerCountryLabel: "Canada",
    otherDomainLabel: "guacmexigrill.ca",
    otherDomainUrl: "https://guacmexigrill.ca",
    cookieName: "guac_geo_prompt_dismissed",
    cookieDays: 30,
  };

  function getCookie(name) {
    var match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return match ? match[2] : null;
  }
  function setCookie(name, value, days) {
    var d = new Date();
    d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = name + "=" + value + ";expires=" + d.toUTCString() + ";path=/";
  }

  if (getCookie(CONFIG.cookieName)) return;

  fetch("/api/geo")
    .then(function (r) { return r.json(); })
    .then(function (data) {
      if (data.country !== CONFIG.triggerCountry) return;
      showBanner();
    })
    .catch(function () {});

  function showBanner() {
    var banner = document.createElement("div");
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-live", "polite");
    banner.style.cssText =
      "position:fixed;bottom:0;left:0;right:0;z-index:9999;background:#151616;" +
      "color:#E2DDCB;padding:16px 20px;display:flex;align-items:center;" +
      "justify-content:center;gap:16px;flex-wrap:wrap;font-family:Arial,sans-serif;" +
      "box-shadow:0 -2px 12px rgba(0,0,0,0.2);";

    banner.innerHTML =
      '<span style="font-size:14px;">Looks like you are browsing from ' +
      CONFIG.triggerCountryLabel +
      ". Visit " + CONFIG.otherDomainLabel + " for your region.</span>" +
      '<a href="' + CONFIG.otherDomainUrl + '" style="background:#D9854A;color:#151616;' +
      'padding:8px 16px;border-radius:4px;text-decoration:none;font-weight:bold;font-size:14px;">' +
      "Visit " + CONFIG.otherDomainLabel + "</a>" +
      '<button id="guac-geo-dismiss" style="background:transparent;color:#E2DDCB;' +
      'border:1px solid #A8AD88;padding:8px 16px;border-radius:4px;cursor:pointer;font-size:14px;">' +
      "Stay here</button>";

    document.body.appendChild(banner);
    document.getElementById("guac-geo-dismiss").addEventListener("click", function () {
      setCookie(CONFIG.cookieName, "1", CONFIG.cookieDays);
      banner.remove();
    });
  }
})();
