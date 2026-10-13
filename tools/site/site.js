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

/* PFM MERMAID INTERACTIVE PATCH v2 -- browser-only, default-on, viewport-lazy Mermaid rendering.
   Does not alter original PNGs or PlantUML views. The atlas source is the source of truth. */
(function () {
  "use strict";

  // Load the engine only when a diagram enters the viewport, not on every page load.
  // This version matches the Mermaid engine recorded by the atlas PNG rendering script.
  const MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@11.16.0/dist/mermaid.esm.min.mjs";
  let enginePromise;
  let renderId = 0;
  let renderQueue = Promise.resolve(); // Prevent simultaneous Mermaid.render calls on long chapters.

  function engine() {
    if (!enginePromise) {
      enginePromise = import(MERMAID_URL).then(function (module) {
        const mermaid = module.default;
        mermaid.initialize({
          startOnLoad: false,
          securityLevel: "strict",
          theme: "default",
          flowchart: { useMaxWidth: false }
        });
        return mermaid;
      }).catch(function (error) {
        enginePromise = null; // Make retry possible after a transient network failure.
        throw error;
      });
    }
    return enginePromise;
  }

  function button(action, caption, title) {
    const element = document.createElement("button");
    element.type = "button";
    element.className = "pfm-live-button";
    element.dataset.action = action;
    element.textContent = caption;
    if (title) element.title = title;
    return element;
  }

  function createViewer(beforeElement, sourceLoader, title) {
    const wrapper = document.createElement("div");
    wrapper.className = "pfm-live-wrapper";

    const pngFigure = beforeElement.matches("figure.diagram") ? beforeElement : null;
    const launch = button("toggle", "Interactive Mermaid", "Show the live Mermaid renderer");
    launch.setAttribute("aria-pressed", "true");
    const pngButton = pngFigure ? button("png", "View original PNG", "Show the pre-rendered diagram") : null;
    if (pngButton) pngButton.setAttribute("aria-pressed", "false");
    const note = document.createElement("span");
    note.className = "pfm-live-note";
    note.textContent = "Live diagram · zoom, pan, and edit source";
    const launchRow = document.createElement("div");
    launchRow.className = "pfm-live-launch";
    launchRow.append(launch);
    if (pngButton) launchRow.append(pngButton);
    launchRow.append(note);
    wrapper.append(launchRow);
    beforeElement.parentNode.insertBefore(wrapper, beforeElement);

    let viewer = null;
    let sourcePromise = null;
    let pristineSource = "";
    let rendering = 0;
    let scale = 1;
    let x = 0;
    let y = 0;
    let chartW = 1000;
    let chartH = 600;

    function getSource() {
      if (!sourcePromise) {
        sourcePromise = Promise.resolve().then(sourceLoader).then(function (value) {
          if (!value || !value.trim()) throw new Error("The Mermaid source is empty.");
          pristineSource = value.replace(/^\uFEFF/, "");
          return pristineSource;
        }).catch(function (error) {
          sourcePromise = null;
          throw error;
        });
      }
      return sourcePromise;
    }

    function build() {
      const panel = document.createElement("section");
      panel.className = "pfm-live-panel";
      panel.setAttribute("aria-label", title + " interactive Mermaid viewer");
      panel.hidden = true;

      const toolbar = document.createElement("div");
      toolbar.className = "pfm-live-toolbar";
      const heading = document.createElement("strong");
      heading.textContent = "Interactive Mermaid";
      toolbar.append(heading);
      toolbar.append(
        button("zoom-out", "−", "Zoom out"),
        button("zoom-in", "+", "Zoom in"),
        button("fit", "Fit", "Fit the diagram in the window"),
        button("edit", "Edit code", "Show or hide the editable source"),
        button("close", "Close", "Close the interactive viewer")
      );
      panel.append(toolbar);

      const stage = document.createElement("div");
      stage.className = "pfm-live-stage";
      stage.tabIndex = 0;
      stage.setAttribute("role", "region");
      stage.setAttribute("aria-label", "Diagram: drag to pan, use the toolbar to zoom, or hold Ctrl and scroll");
      const surface = document.createElement("div");
      surface.className = "pfm-live-surface";
      stage.append(surface);
      panel.append(stage);

      const status = document.createElement("p");
      status.className = "pfm-live-status";
      status.setAttribute("role", "status");
      status.textContent = "Loading original Mermaid source…";
      panel.append(status);

      const editorRegion = document.createElement("div");
      editorRegion.className = "pfm-live-editor";
      editorRegion.hidden = true;
      const label = document.createElement("label");
      const editor = document.createElement("textarea");
      editor.spellcheck = false;
      editor.rows = 14;
      editor.className = "pfm-live-code";
      const editorId = "pfm-live-code-" + (++renderId);
      editor.id = editorId;
      label.htmlFor = editorId;
      label.textContent = "Mermaid source (edits stay in this browser tab):";
      editorRegion.append(label, editor);
      const editorActions = document.createElement("div");
      editorActions.className = "pfm-live-toolbar pfm-live-editor-actions";
      editorActions.append(button("render", "Render changes", "Render the edited Mermaid source"),
                           button("restore", "Restore original", "Restore the repository source"));
      editorRegion.append(editorActions);
      panel.append(editorRegion);
      wrapper.append(panel);

      function applyTransform() {
        surface.style.transform = "translate(" + x + "px," + y + "px) scale(" + scale + ")";
      }
      function fit() {
        if (!surface.querySelector("svg")) return;
        const w = stage.clientWidth;
        const h = stage.clientHeight;
        if (!w || !h) return;
        scale = Math.min((w - 32) / chartW, (h - 32) / chartH, 1.5);
        scale = Math.max(scale, 0.015);
        x = (w - chartW * scale) / 2;
        y = (h - chartH * scale) / 2;
        applyTransform();
      }
      function zoomAt(factor, localX, localY) {
        const next = Math.max(0.015, Math.min(8, scale * factor));
        x = localX - ((localX - x) / scale) * next;
        y = localY - ((localY - y) / scale) * next;
        scale = next;
        applyTransform();
      }
      function centerZoom(factor) {
        zoomAt(factor, stage.clientWidth / 2, stage.clientHeight / 2);
      }
      async function render() {
        const request = ++rendering;
        status.textContent = "Rendering the Mermaid source in your browser…";
        try {
          // Serialize Mermaid renders; several diagrams may enter view together.
          const sourceSnapshot = editor.value;
          const job = renderQueue.catch(function () {}).then(async function () {
            const mermaid = await engine();
            return mermaid.render("pfm-live-svg-" + (++renderId), sourceSnapshot);
          });
          renderQueue = job.catch(function () {});
          const output = await job;
          if (request !== rendering) return false;
          surface.innerHTML = output.svg;
          if (typeof output.bindFunctions === "function") output.bindFunctions(surface);
          const svg = surface.querySelector("svg");
          if (!svg) throw new Error("The renderer did not produce a diagram.");
          const viewBox = svg.viewBox && svg.viewBox.baseVal;
          chartW = viewBox && viewBox.width > 0 ? viewBox.width : (parseFloat(svg.getAttribute("width")) || 1000);
          chartH = viewBox && viewBox.height > 0 ? viewBox.height : (parseFloat(svg.getAttribute("height")) || 600);
          svg.style.width = chartW + "px";
          svg.style.height = chartH + "px";
          svg.style.maxWidth = "none";
          fit();
          status.textContent = "Rendered in your browser. Drag to pan, use +/− to zoom, or Ctrl + wheel.";
          return true;
        } catch (error) {
          if (request !== rendering) return false;
          status.textContent = "Unable to render: " + (error && error.message ? error.message : String(error)) +
            ". The original PNG is available as a fallback.";
          return false;
        }
      }

      toolbar.addEventListener("click", function (event) {
        const action = event.target.closest("button[data-action]")?.dataset.action;
        if (action === "zoom-out") centerZoom(1 / 1.25);
        if (action === "zoom-in") centerZoom(1.25);
        if (action === "fit") fit();
        if (action === "edit") {
          editorRegion.hidden = !editorRegion.hidden;
          toolbar.querySelector('[data-action="edit"]').setAttribute("aria-pressed", String(!editorRegion.hidden));
          if (!editorRegion.hidden) editor.focus();
        }
        if (action === "close") {
          if (pngFigure) {
            selectPng();
          } else {
            panel.hidden = true;
            launch.setAttribute("aria-pressed", "false");
          }
          launch.focus();
        }
      });
      editorActions.addEventListener("click", function (event) {
        const action = event.target.closest("button[data-action]")?.dataset.action;
        if (action === "render") void render();
        if (action === "restore") { editor.value = pristineSource; void render(); }
      });
      editor.addEventListener("keydown", function (event) {
        if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
          event.preventDefault(); void render();
        }
      });
      stage.addEventListener("wheel", function (event) {
        if (!event.ctrlKey) return; // Preserve normal page scrolling.
        event.preventDefault();
        const rect = stage.getBoundingClientRect();
        zoomAt(event.deltaY < 0 ? 1.13 : 1 / 1.13, event.clientX - rect.left, event.clientY - rect.top);
      }, { passive: false });
      let drag = null;
      stage.addEventListener("pointerdown", function (event) {
        if (event.button !== 0) return;
        drag = { id: event.pointerId, px: event.clientX, py: event.clientY, x: x, y: y };
        stage.setPointerCapture(event.pointerId);
        stage.classList.add("is-dragging");
      });
      stage.addEventListener("pointermove", function (event) {
        if (!drag || event.pointerId !== drag.id) return;
        x = drag.x + event.clientX - drag.px;
        y = drag.y + event.clientY - drag.py;
        applyTransform();
      });
      function stopDrag() { drag = null; stage.classList.remove("is-dragging"); }
      stage.addEventListener("pointerup", stopDrag);
      stage.addEventListener("pointercancel", stopDrag);
      stage.addEventListener("lostpointercapture", stopDrag);
      stage.addEventListener("keydown", function (event) {
        if (event.key === "+" || event.key === "=") { event.preventDefault(); centerZoom(1.25); }
        if (event.key === "-") { event.preventDefault(); centerZoom(1 / 1.25); }
        if (event.key === "0") { event.preventDefault(); fit(); }
        const pan = 45;
        if (event.key === "ArrowLeft") { x += pan; event.preventDefault(); applyTransform(); }
        if (event.key === "ArrowRight") { x -= pan; event.preventDefault(); applyTransform(); }
        if (event.key === "ArrowUp") { y += pan; event.preventDefault(); applyTransform(); }
        if (event.key === "ArrowDown") { y -= pan; event.preventDefault(); applyTransform(); }
      });
      window.addEventListener("resize", function () { if (!panel.hidden) fit(); });
      return { panel: panel, editor: editor, render: render };
    }

    // A viewer is the default, rather than a second view below an always-visible PNG.
    // Build its controls immediately; initialize the drawing only near the viewport.
    viewer = build();
    viewer.panel.hidden = false;
    if (pngFigure) pngFigure.hidden = true;
    let successful = false;
    let pending = null;

    function selectPng(message) {
      if (!pngFigure) return;
      pngFigure.hidden = false;
      viewer.panel.hidden = true;
      launch.setAttribute("aria-pressed", "false");
      pngButton.setAttribute("aria-pressed", "true");
      if (message) note.textContent = message;
      else note.textContent = "Original PNG image";
    }

    function selectInteractive() {
      if (pngFigure) pngFigure.hidden = true;
      viewer.panel.hidden = false;
      launch.setAttribute("aria-pressed", "true");
      if (pngButton) pngButton.setAttribute("aria-pressed", "false");
      note.textContent = "Live diagram · zoom, pan, and edit source";
    }

    function ensureRendered() {
      if (successful) return Promise.resolve(true);
      if (pending) return pending;
      pending = (async function () {
        try {
          viewer.editor.value = await getSource();
          const ok = await viewer.render();
          if (!ok) {
            if (pngFigure) selectPng("Live rendering unavailable · showing original PNG");
            return false;
          }
          successful = true;
          return true;
        } catch (error) {
          viewer.panel.querySelector(".pfm-live-status").textContent = "Unable to load Mermaid source: " +
            (error && error.message ? error.message : String(error));
          if (pngFigure) selectPng("Live rendering unavailable · showing original PNG");
          return false;
        } finally {
          pending = null;
        }
      })();
      return pending;
    }

    launch.addEventListener("click", function () {
      selectInteractive();
      void ensureRendered();
    });
    if (pngButton) {
      pngButton.addEventListener("click", function () { selectPng(); });
    }

    // An offline/no-JavaScript visitor sees the PNG, because it is hidden only
    // after this script actually creates the live viewer successfully.
    // Chapter pages may contain many diagrams; don't render all simultaneously.
    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(function (entries) {
        if (!entries.some(function (entry) { return entry.isIntersecting; })) return;
        observer.disconnect();
        if (!viewer.panel.hidden) void ensureRendered();
      }, { rootMargin: "350px 0px" });
      observer.observe(wrapper);
    } else {
      void ensureRendered();
    }
  }

  // Current atlas figures. The existing 'Code file' anchor identifies Mermaid versus PlantUML.
  document.querySelectorAll("figure.diagram[id^='figure-']").forEach(function (figure) {
    const preceding = figure.previousElementSibling;
    let sourceAnchor = preceding && preceding.querySelector('a[href$=".mmd"]');
    if (!sourceAnchor && document.querySelectorAll("figure.diagram").length === 1) {
      sourceAnchor = document.querySelector('.copy-row a[href$=".mmd"]');
    }
    if (!sourceAnchor) return; // PlantUML stays as its existing PNG.
    const sourceUrl = sourceAnchor.href;
    createViewer(figure, async function () {
      const response = await fetch(sourceUrl);
      if (!response.ok) throw new Error("Source request failed (HTTP " + response.status + ")");
      return response.text();
    }, figure.id.replace(/^figure-/, "Diagram "));
  });

  // Supplementary historical models have editable source but no authoritative PNG.
  // Reuse that source without confusing their IDs with current atlas diagrams.
  document.querySelectorAll("pre.model-code").forEach(function (pre) {
    const code = pre.querySelector("code.model-source");
    if (!code || !document.querySelector('a[download][href$=".mmd"]')) return;
    createViewer(pre, function () { return code.textContent; }, "Historical research model");
  });
})();
/* END PFM MERMAID INTERACTIVE PATCH v2 */
