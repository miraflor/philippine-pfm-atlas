// Philippine PFM Atlas: search in the text of all pages. The index is the file assets/search-index.json.
(function () {
  "use strict";
  var form = document.getElementById("search-form");
  var input = document.getElementById("q");
  var status = document.getElementById("search-status");
  var list = document.getElementById("results");
  var index = null;

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function escapeRegExp(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
  function count(haystack, needle) {
    var n = 0, i = haystack.indexOf(needle);
    while (i !== -1 && n < 10) { n += 1; i = haystack.indexOf(needle, i + needle.length); }
    return n;
  }

  function snippet(text, terms) {
    var lower = text.toLowerCase();
    var at = -1;
    terms.forEach(function (t) { var i = lower.indexOf(t); if (i !== -1 && (at === -1 || i < at)) { at = i; } });
    var start = Math.max(0, at - 90);
    var end = Math.min(text.length, (at === -1 ? 0 : at) + 170);
    var piece = (start > 0 ? "… " : "") + text.slice(start, end) + (end < text.length ? " …" : "");
    var html = escapeHtml(piece);
    var pattern = new RegExp("(" + terms.map(function (t) { return escapeRegExp(escapeHtml(t)); }).join("|") + ")", "gi");
    return html.replace(pattern, "<mark>$1</mark>");
  }

  function run(query) {
    var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    list.innerHTML = "";
    if (!terms.length) { status.textContent = "Type one or more words, a code or a form name."; return; }
    var hits = [];
    index.forEach(function (e, n) {
      var title = e.tl, page = e.pl, text = e.xl;
      var score = 0;
      for (var i = 0; i < terms.length; i += 1) {
        var t = terms[i];
        var inTitle = title.indexOf(t) !== -1, inPage = page.indexOf(t) !== -1, inText = count(text, t);
        if (!inTitle && !inPage && !inText) { return; }
        score += (inTitle ? 20 : 0) + (inPage ? 5 : 0) + inText;
      }
      hits.push({ e: e, score: score, n: n });
    });
    hits.sort(function (a, b) { return b.score - a.score || a.n - b.n; });
    var shown = hits.slice(0, 60);
    status.textContent = hits.length === 0 ? "No result for “" + query + "”." :
      hits.length + (hits.length === 1 ? " result" : " results") + " for “" + query + "”" +
      (hits.length > shown.length ? ". The first " + shown.length + " are shown." : ".");
    shown.forEach(function (h) {
      var li = document.createElement("li");
      li.innerHTML = '<a href="' + escapeHtml(h.e.u) + '">' + escapeHtml(h.e.t) + "</a>" +
        '<span class="where">' + escapeHtml(h.e.p) + "</span>" +
        '<span class="snippet">' + snippet(h.e.x, terms) + "</span>";
      list.appendChild(li);
    });
  }

  var query = new URLSearchParams(window.location.search).get("q") || "";
  input.value = query;
  status.textContent = "Loading the index …";
  fetch("assets/search-index.json").then(function (r) { return r.json(); }).then(function (data) {
    index = data.map(function (e) {
      return { t: e.t, p: e.p, u: e.u, x: e.x, tl: e.t.toLowerCase(), pl: e.p.toLowerCase(), xl: e.x.toLowerCase() };
    });
    run(query);
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var q = input.value.trim();
      history.replaceState(null, "", "search.html" + (q ? "?q=" + encodeURIComponent(q) : ""));
      run(q);
    });
  }).catch(function () {
    status.textContent = "The search index could not be loaded. Search works when the website is served by a web server, for example GitHub Pages.";
  });
})();
