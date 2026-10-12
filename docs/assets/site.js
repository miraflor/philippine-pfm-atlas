// Philippine PFM Atlas: small aids on the pages. Every page can also be read without JavaScript.
(function () {
  "use strict";

  // Site preference is opt-in. Never infer dark mode from operating-system settings.
  var themeButton = document.getElementById("theme-toggle");
  if (themeButton) {
    function syncThemeButton() {
      var dark = document.documentElement.getAttribute("data-theme") === "dark";
      themeButton.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
      themeButton.textContent = dark ? "Light mode" : "Dark mode";
    }
    syncThemeButton();
    themeButton.addEventListener("click", function () {
      var newTheme = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", newTheme);
      try { window.localStorage.setItem("pfm-atlas-theme", newTheme); } catch (error) { /* preference still applies this visit */ }
      syncThemeButton();
    });
  }

  // Copy the code of a diagram.
  document.querySelectorAll("button[data-copy]").forEach(function (button) {
    button.addEventListener("click", function () {
      var target = document.getElementById(button.getAttribute("data-copy"));
      if (!target || !navigator.clipboard) { return; }
      navigator.clipboard.writeText(target.textContent).then(function () {
        var label = button.textContent;
        button.textContent = "Copied";
        setTimeout(function () { button.textContent = label; }, 1500);
      });
    });
  });

  // Reference G: show the points of one status.
  document.querySelectorAll(".filter[data-filter]").forEach(function (group) {
    var buttons = group.querySelectorAll("button[data-status]");
    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        var status = button.getAttribute("data-status");
        buttons.forEach(function (b) { b.setAttribute("aria-pressed", b === button ? "true" : "false"); });
        document.querySelectorAll("tr[data-status]").forEach(function (row) {
          row.hidden = !(status === "all" || row.getAttribute("data-status") === status);
        });
      });
    });
  });

  // List of diagrams: filter by words.
  var input = document.getElementById("diagram-filter");
  if (input) {
    var items = document.querySelectorAll(".diagram-list li");
    var count = document.getElementById("diagram-count");
    var groups = document.querySelectorAll("section.diagram-group");
    input.addEventListener("input", function () {
      var words = input.value.toLowerCase().split(/\s+/).filter(Boolean);
      var shown = 0;
      items.forEach(function (item) {
        var text = item.textContent.toLowerCase();
        var ok = words.every(function (w) { return text.indexOf(w) !== -1; });
        item.hidden = !ok;
        if (ok) { shown += 1; }
      });
      groups.forEach(function (g) {
        g.hidden = g.querySelectorAll("li:not([hidden])").length === 0;
      });
      if (count) { count.textContent = shown + " of " + items.length + " diagrams"; }
    });
  }
  // Progressive enhancement: source-linked image opens in an accessible native dialog.
  document.querySelectorAll("figure.diagram > a:has(img)").forEach(function (link) {
    link.addEventListener("click", function (event) {
      if (typeof HTMLDialogElement === "undefined" || !HTMLDialogElement.prototype.showModal) return;
      event.preventDefault();
      var dialog = document.getElementById("atlas-zoom");
      if (!dialog) {
        dialog = document.createElement("dialog"); dialog.id = "atlas-zoom";
        dialog.innerHTML = '<div class="zoom-toolbar"><strong>Diagram preview</strong><button type="button" aria-label="Close enlarged image">Close ×</button></div><img alt="Enlarged diagram">';
        document.body.appendChild(dialog);
        dialog.querySelector("button").addEventListener("click", function () {dialog.close();});
        dialog.addEventListener("click", function(e){ if(e.target===dialog) dialog.close(); });
      }
      dialog.querySelector("img").src = link.href;
      dialog.querySelector("img").alt = link.querySelector("img").alt;
      dialog.showModal();
    });
  });
  document.addEventListener("keydown", function(event) {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase()==="k") {
      var field = document.querySelector(".header-search input[type=search]");
      if (field) { event.preventDefault(); field.focus(); field.select(); }
    }
  });
})();
