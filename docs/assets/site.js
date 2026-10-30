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

  // Research models: the viewer reads the code shown on the page.
  document.querySelectorAll("pre.model-code").forEach(function (pre) {
    const code = pre.querySelector("code.model-source");
    if (!code || !document.querySelector('a[download][href$=".mmd"]')) return;
    createViewer(pre, function () { return code.textContent; }, "Research model");
  });
})();
/* END PFM MERMAID INTERACTIVE PATCH v2 */

/* Philippine PFM Atlas editorial experience. Progressive enhancement only. */
(function () {
  'use strict';
  var hasExperience = document.querySelector('[data-atlas-experience="1"]');
  if (!hasExperience) return;

  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduceMotion && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('atlas-motion');
    var reveal = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in-view');
          reveal.unobserve(entry.target);
        }
      });
    }, { threshold: 0.04, rootMargin: '0px 0px 60px 0px' });
    document.querySelectorAll('.atlas-story-section, .atlas-lesson-scene, .atlas-diagram-group').forEach(function (element) {
      reveal.observe(element);
    });
  }

  var lineMap = document.querySelector('.home #lines .map[data-highlight-line]');
  if (lineMap) {
    document.querySelectorAll('.atlas-map-controls button[data-atlas-line]').forEach(function (button) {
      button.addEventListener('click', function () {
        lineMap.dataset.highlightLine = button.dataset.atlasLine;
        document.querySelectorAll('.atlas-map-controls button').forEach(function (other) {
          other.setAttribute('aria-pressed', String(other === button));
        });
      });
    });
  }

  var orbit = document.querySelector('.atlas-orbit');
  var scenes = Array.prototype.slice.call(document.querySelectorAll('.atlas-lesson-scene'));
  if (orbit && scenes.length) {
    var active = -1;
    var portrait = document.getElementById('atlas-active-diagram');
    var previewLink = document.getElementById('atlas-active-diagram-link');
    var number = document.getElementById('atlas-active-number');

    function activate(index) {
      if (active === index || index < 0 || index >= scenes.length) return;
      active = index;
      var scene = scenes[index];
      scenes.forEach(function (s, i) { s.classList.toggle('is-active', i === index); });
      orbit.querySelectorAll('[data-orbit]').forEach(function (node) {
        node.classList.toggle('is-active', Number(node.dataset.orbit) === index + 1);
      });
      if (number) number.textContent = String(index + 1).padStart(2, '0') + ' / ' + String(scenes.length).padStart(2, '0');
      if (portrait) {
        var url = scene.dataset.preview;
        if (portrait.getAttribute('src') !== url) portrait.setAttribute('src', url);
        portrait.setAttribute('alt', 'Diagram ' + scene.dataset.previewId + ': ' + scene.dataset.previewTitle);
      }
      if (previewLink) {
        previewLink.href = 'diagrams/' + encodeURIComponent(scene.dataset.previewId) + '.html';
        previewLink.textContent = 'Explore diagram ' + scene.dataset.previewId + ' ↗';
      }
    }

    var ticking = false;
    function syncCurrentScene() {
      ticking = false;
      var targetY = window.innerHeight * 0.48;
      var best = 0;
      var bestDistance = Infinity;
      scenes.forEach(function (scene, i) {
        var bounds = scene.getBoundingClientRect();
        var distance = bounds.top <= targetY && bounds.bottom >= targetY ? 0 :
          Math.min(Math.abs(bounds.top - targetY), Math.abs(bounds.bottom - targetY));
        if (distance < bestDistance) { bestDistance = distance; best = i; }
      });
      activate(best);
    }
    function onPositionChange() {
      if (!ticking) { ticking = true; window.requestAnimationFrame(syncCurrentScene); }
    }
    window.addEventListener('scroll', onPositionChange, {passive:true});
    window.addEventListener('resize', onPositionChange);
    activate(0);
    onPositionChange();
  }

  if (document.querySelector('.home.atlas-experience')) {
    var meter = document.createElement('div');
    meter.className = 'atlas-scroll-meter';
    meter.setAttribute('aria-hidden', 'true');
    var bar = document.createElement('span');
    meter.appendChild(bar);
    document.body.appendChild(meter);
    var busy = false;
    function updateMeter() {
      busy = false;
      var max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
      var pct = Math.min(1, Math.max(0, window.scrollY / max));
      bar.style.transform = 'scaleX(' + pct.toFixed(4) + ')';
    }
    window.addEventListener('scroll', function () {
      if (!busy) { busy = true; window.requestAnimationFrame(updateMeter); }
    }, {passive:true});
    updateMeter();
  }
})();

/* PH PFM Atlas Mermaid theater view v1.
   Non-invasive enhancement of the existing default-on Mermaid viewer.
   No renderer downloads, changed diagram sources or extra dependencies. */
(function () {
  'use strict';

  // The existing Mermaid viewer constructs all panels before this script runs.
  // Attaching to its toolbar retains the existing zoom, pan, editor and PNG view.
  var panels = document.querySelectorAll('.pfm-live-panel');
  panels.forEach(function (panel) {
    var toolbar = panel.querySelector('.pfm-live-toolbar');
    var fitButton = toolbar && toolbar.querySelector('[data-action="fit"]');
    if (!toolbar || !fitButton || toolbar.querySelector('[data-action="theater"]')) return;

    var theaterButton = document.createElement('button');
    theaterButton.type = 'button';
    theaterButton.className = 'pfm-live-button';
    theaterButton.dataset.action = 'theater';
    theaterButton.textContent = 'Theater view';
    theaterButton.title = 'Expand the interactive diagram to fill the screen';
    theaterButton.setAttribute('aria-pressed', 'false');
    var editorButton = toolbar.querySelector('[data-action="edit"]');
    toolbar.insertBefore(theaterButton, editorButton || toolbar.lastElementChild);

    var fallback = false;
    var previouslyActive = false;
    function isActive() { return document.fullscreenElement === panel || fallback; }
    function refit() {
      if (panel.hidden) return;
      // Fullscreen layout must settle before measuring the stage dimensions.
      requestAnimationFrame(function () { requestAnimationFrame(function () { fitButton.click(); }); });
    }
    function update() {
      var active = isActive();
      theaterButton.textContent = active ? 'Exit theater' : 'Theater view';
      theaterButton.title = active ? 'Return the diagram to its normal page size' : 'Expand the diagram to fill the screen';
      theaterButton.setAttribute('aria-pressed', String(active));
      if (active !== previouslyActive) refit();
      previouslyActive = active;
    }
    function exitFallback() {
      if (!fallback) return;
      fallback = false;
      panel.classList.remove('atlas-theater-fallback');
      document.documentElement.classList.remove('atlas-theater-open');
      update();
    }
    function enterFallback() {
      fallback = true;
      panel.classList.add('atlas-theater-fallback');
      document.documentElement.classList.add('atlas-theater-open');
      update();
    }
    theaterButton.addEventListener('click', function () {
      if (fallback) { exitFallback(); return; }
      if (document.fullscreenElement === panel) {
        if (document.exitFullscreen) {
          document.exitFullscreen().catch(function () { update(); });
        } else update();
        return;
      }
      // User gesture is required: call the Fullscreen API inside this click handler.
      if (typeof panel.requestFullscreen === 'function') {
        try {
          var result = panel.requestFullscreen();
          if (result && result.catch) result.catch(function () { enterFallback(); });
        } catch (error) { enterFallback(); }
      } else enterFallback();
    });
    document.addEventListener('fullscreenchange', function () { update(); });
    toolbar.addEventListener('click', function (event) {
      var button = event.target.closest && event.target.closest('button[data-action]');
      if (button && button.dataset.action === 'edit' && isActive()) refit();
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && fallback) { event.preventDefault(); exitFallback(); }
    });
    // If an existing viewer button switches to PNG or closes the panel, leave
    // theater mode first so the user never gets stuck in an empty fullscreen view.
    toolbar.addEventListener('click', function (event) {
      var button = event.target.closest && event.target.closest('button[data-action]');
      if (button && button.dataset.action === 'close') {
        if (fallback) exitFallback();
        else if (document.fullscreenElement === panel && document.exitFullscreen) {
          document.exitFullscreen().catch(function () {});
        }
      }
    }, true);
    var wrapper = panel.closest('.pfm-live-wrapper');
    var pngButton = wrapper && wrapper.querySelector('[data-action="png"]');
    if (pngButton) pngButton.addEventListener('click', function () {
      if (fallback) exitFallback();
      else if (document.fullscreenElement === panel && document.exitFullscreen) {
        document.exitFullscreen().catch(function () {});
      }
    }, true);
    update();
  });
})();
/* END PH PFM Atlas Mermaid theater view v1 */

/* PFM ATLAS SIMPLE SITE-WIDE NAVIGATION â€” October 2026.
   One thin fixed Explore Atlas bar on every page; one contextual right-hand TOC.
   No duplicate floating site menu or left rail. All destinations remain unchanged. */
(function () {
  'use strict';
  var header = document.querySelector('.site-header');
  var bar = header && header.querySelector('.header-row');
  var siteNav = header && header.querySelector('nav.site-nav');
  var main = document.getElementById('main');
  if (!header || !bar || !siteNav || !main) return;

  // Move, do not clone: original site links, active-page attributes and keyboard links survive.
  var theme = document.getElementById('theme-toggle');
  var menu = document.createElement('button');
  menu.type = 'button';
  menu.className = 'atlas-top-menu';
  menu.setAttribute('aria-controls', 'atlas-global-links');
  menu.setAttribute('aria-expanded', 'false');
  menu.textContent = 'Explore Atlas';
  siteNav.id = 'atlas-global-links';
  bar.insertBefore(menu, theme);
  bar.insertBefore(siteNav, menu);
  document.body.classList.add('atlas-topbar-active');

  function closeMenu() {
    header.classList.remove('atlas-top-menu-open');
    menu.setAttribute('aria-expanded','false');
  }
  menu.addEventListener('click', function () {
    var open = !header.classList.contains('atlas-top-menu-open');
    header.classList.toggle('atlas-top-menu-open', open);
    menu.setAttribute('aria-expanded', String(open));
  });
  siteNav.addEventListener('click', function (event) {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('click', function (event) {
    if (!header.contains(event.target)) closeMenu();
  });

  // The single page navigator is populated from existing authored anchors/TOCs.
  // Do not generate replacement navigation for the entire site or duplicate content.
  function link(id, label) {
    var a = document.createElement('a'); a.href='#'+id; a.textContent=label; return a;
  }
  function pageLinks() {
    // Walkthrough: derive the eight real authored scene anchors, never build labels
    // by concatenating a Unicode separator (which can become 'A-circumflex dot').
    var lessons = main.querySelectorAll('.atlas-lesson-scene[id]');
    if (lessons.length) {
      var labels = [
        'See the whole system', 'From a priority to the GAA',
        'Authority versus cash', 'When payment becomes due',
        'How public money moves', 'Records and audit',
        'LGUs, GOCCs, payroll and risks', 'UACS, IFMIS and interfaces'
      ];
      return Array.prototype.map.call(lessons, function (lesson, i) {
        var h = lesson.querySelector('h2');
        var full = h ? h.textContent.trim() : 'Lesson';
        var anchor = link(lesson.id, '');
        anchor.className = 'atlas-page-lesson-link';
        anchor.title = full;
        anchor.setAttribute('aria-label', 'Lesson ' + String(i + 1).padStart(2, '0') + ': ' + full);
        var number = document.createElement('span');
        number.className = 'atlas-page-lesson-number';
        number.textContent = String(i + 1).padStart(2, '0');
        var title = document.createElement('span');
        title.className = 'atlas-page-lesson-name';
        title.textContent = labels[i] || full;
        anchor.appendChild(number);
        anchor.appendChild(title);
        return anchor;
      });
    }

    // Diagram catalogue: its phase sections have genuine IDs on the containing
    // section, not on its H2. The generic H2[id] scanner therefore misses them.
    var catalogue = main.querySelector('[data-cycle-catalog="diagrams"]');
    if (catalogue) {
      var groups = [
        ['preparation', 'Preparation'],
        ['legislation', 'Legislation'],
        ['execution', 'Execution'],
        ['accountability', 'Accountability'],
        ['across', 'Shared diagrams']
      ];
      return groups.filter(function (group) {
        return !!document.getElementById('cycle-diagrams-' + group[0]);
      }).map(function (group) {
        var anchor = link('cycle-diagrams-' + group[0], group[1]);
        anchor.className = 'atlas-page-diagram-phase-link';
        return anchor;
      });
    }

    var original = document.querySelector('.atlas-page-wayfinder');
    if (original) return Array.prototype.slice.call(original.querySelectorAll('a[href^="#"]'));
    var toc = document.querySelector('.doc-side nav.toc');
    if (toc) {
      var major = Array.prototype.slice.call(toc.querySelectorAll('a[href^="#"]')).filter(function (a) {
        var target = document.getElementById(a.getAttribute('href').slice(1));
        return target && target.tagName === 'H2';
      });
      if (major.length) return major;
    }
    var headings = main.querySelectorAll('h2[id]');
    if (headings.length) return Array.prototype.map.call(headings, function (h) {
      return link(h.id, h.textContent.trim());
    });
    return [];
  }
  var choices = pageLinks().filter(function (a) {
    var href = a.getAttribute('href') || '';
    return href[0]==='#' && document.getElementById(href.slice(1));
  }).slice(0,20);
  // Do not synthesize a floating navigation for pages without an authored outline.
  var hasPageOutline = (new Set(choices.map(function (item) {
    return item.getAttribute('href');
  }))).size >= 2;

  var rail = document.createElement('nav');
  rail.className='atlas-page-float';
  rail.setAttribute('aria-label','On this page');
  var heading=document.createElement('div');
  heading.className='atlas-page-float-head';
  heading.textContent='ON THIS PAGE';
  rail.appendChild(heading);
  var button=document.createElement('button');
  button.type='button'; button.className='atlas-page-float-toggle';
  button.setAttribute('aria-expanded','false');
  button.setAttribute('aria-label','Open page sections');
  button.textContent='On this page';
  rail.appendChild(button);
  var list=document.createElement('div');
  list.className='atlas-page-float-links';
  choices.forEach(function (a) {list.appendChild(a.cloneNode(true));});
  rail.appendChild(list);
  if (choices.length >= 2) document.body.appendChild(rail);
  var floatLinks=Array.prototype.slice.call(list.querySelectorAll('a'));
  var sections=floatLinks.map(function (a) {return document.getElementById(a.hash.slice(1));});
  var raf=false;
  function update() {
    raf=false;
    var offset=header.getBoundingClientRect().height + 36;
    var active=0;
    sections.forEach(function (section,i) {
      if (section && section.getBoundingClientRect().top < offset + window.innerHeight*.28) active=i;
    });
    floatLinks.forEach(function (a,i) {
      if (i===active) a.setAttribute('aria-current','location');
      else a.removeAttribute('aria-current');
    });
  }
  function schedule(){if(!raf){raf=true;requestAnimationFrame(update);}}
  function syncHeight() {
    document.documentElement.style.setProperty('--atlas-topbar-height', Math.ceil(bar.getBoundingClientRect().height)+'px');
    schedule();
  }
  button.addEventListener('click', function () {
    var expanded=button.getAttribute('aria-expanded')!=='true';
    rail.classList.toggle('is-open',expanded);
    button.setAttribute('aria-expanded',String(expanded));
  });
  list.addEventListener('click', function (event) {
    if (event.target.closest('a')) {
      rail.classList.remove('is-open');
      button.setAttribute('aria-expanded','false');
    }
  });
  document.addEventListener('keydown', function (event) {
    if (event.key==='Escape') {closeMenu();rail.classList.remove('is-open');button.setAttribute('aria-expanded','false');}
  });
  window.addEventListener('resize',function(){syncHeight();closeMenu();});
  window.addEventListener('scroll',schedule,{passive:true});
  window.addEventListener('hashchange',schedule);
  if (window.ResizeObserver) new ResizeObserver(syncHeight).observe(bar);
  syncHeight();
  window.addEventListener('load',syncHeight);
})();
/* PFM NAV LABEL + OUTLINE FIX v2 */
/* PFM WALKTHROUGH SIMPLIFICATION v1 */
/* PFM ATLAS ASCII LESSONS + DIAGRAM OUTLINE 2026-10 v3 */

/* PFM-CHAPTER-DUAL-FLOAT-2026-10-30: chapter catalogue left, local outline right. */
(function () {
  'use strict';
  var match = /\/chapters\/([A-Z][A-Z0-9]*)\.html$/i.exec(location.pathname);
  if (!match) return;
  var chapterId = match[1].toUpperCase();
  var article = document.querySelector('main .doc article.prose');
  var right = document.querySelector('.atlas-page-float');
  if (!article || !right) return;
  var headings = Array.prototype.slice.call(article.querySelectorAll('h2[id], h3[id]'));
  if (!headings.length) return;
  document.body.classList.add('atlas-dual-chapter-nav');

  // The chapter catalogue comes from budget_cycle_nav.PHASES when the patch is installed.
  var chapters = [{"label":"Preparation","items":[["P0","Preparation overview"],["P1","Budget Call"],["P2","Citizen engagement"],["P3","Regional Development Council consultations"],["P4","Program convergence"],["P5","Agency Tier 1 proposals: ongoing expenditures"],["P6","Tier 1 deliberations"],["P7","Budget Priorities Framework"],["P8","Agency Tier 2 proposals: new or expanded spending"],["P9","Tier 2 deliberations"],["P10","Presentation to the President and Cabinet"],["P11","Confirmation and finalization"],["P12","The President's Budget submitted to Congress"]]},{"label":"Legislation","items":[["L0","Legislation overview"],["L1","House deliberations"],["L2","Senate deliberations"],["L3","Bicameral deliberations"],["L4","Ratification and enrolment"],["L5","Enactment of the General Appropriations Act"]]},{"label":"Execution","items":[["E0","Execution overview"],["E1","Early procurement activities"],["E2","Budget execution program"],["E3","Allotment release"],["E4","Obligation"],["E5","Cash allocation"],["E6","Disbursement"]]},{"label":"Accountability","items":[["A0","Accountability overview"],["A1","Performance targets"],["A2","Citizen engagement"],["A3","Monitoring and evaluation"],["A4","Agencies' accountability reports"],["A5","Performance review"],["A6","In-year reports"],["A7","DBCC Mid-Year Report"],["A8","DBCC Year-End Report"],["A9","Audit report"]]},{"label":"Shared chapters","items":[["IS","Information systems and IFMIS"],["UACS","UACS and record identifiers"]]}];
  var left = document.createElement('nav');
  left.className = 'atlas-chapter-catalog-float';
  left.setAttribute('aria-label','All chapters');
  var title = document.createElement('div');
  title.className = 'atlas-chapter-catalog-head';
  title.textContent = 'ALL CHAPTERS';
  left.appendChild(title);
  var toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = 'atlas-chapter-catalog-toggle';
  toggle.setAttribute('aria-expanded','false');
  toggle.setAttribute('aria-label','Show all chapters');
  toggle.textContent = 'All chapters';
  left.appendChild(toggle);
  var all = document.createElement('div');
  all.className = 'atlas-chapter-catalog-list';
  var current = null;
  chapters.forEach(function (phase) {
    var group = document.createElement('section');
    group.className = 'atlas-chapter-catalog-group';
    var groupTitle = document.createElement('p');
    groupTitle.className = 'atlas-chapter-catalog-phase';
    groupTitle.textContent = phase.label;
    group.appendChild(groupTitle);
    phase.items.forEach(function (item) {
      var a = document.createElement('a');
      a.href = item[0] + '.html';
      var code = document.createElement('span');
      code.className = 'atlas-chapter-catalog-id';
      code.textContent = item[0];
      var label = document.createElement('span');
      label.className = 'atlas-chapter-catalog-name';
      label.textContent = item[1];
      a.appendChild(code);
      a.appendChild(label);
      if (item[0] === chapterId) {
        a.setAttribute('aria-current','page');
        current = a;
      }
      group.appendChild(a);
    });
    all.appendChild(group);
  });
  left.appendChild(all);
  document.body.appendChild(left);
  function close() {left.classList.remove('is-open'); toggle.setAttribute('aria-expanded','false');}
  toggle.addEventListener('click', function () {
    var open = !left.classList.contains('is-open');
    left.classList.toggle('is-open',open); toggle.setAttribute('aria-expanded',String(open));
  });
  all.addEventListener('click',function (event) {if (event.target.closest('a')) close();});
  document.addEventListener('keydown',function (event) {if(event.key === 'Escape') close();});
  document.addEventListener('click',function (event) {if (!left.contains(event.target)) close();});
  if (current) requestAnimationFrame(function () {
    all.scrollTop = Math.max(0, current.getBoundingClientRect().top - all.getBoundingClientRect().top + all.scrollTop - all.clientHeight / 2);
  });

  // Keep the original right-hand On this page float. Expand only the active section's subsections.
  var list = right.querySelector('.atlas-page-float-links');
  if (!list) return;
  var group = null, records = [], links = {};
  var fragment = document.createDocumentFragment();
  headings.forEach(function (heading) {
    if (heading.tagName === 'H2' || !group) {
      group = document.createElement('div');
      group.className = 'atlas-chapter-page-group';
      var major = document.createElement('a');
      major.href = '#' + heading.id;
      major.className = 'atlas-chapter-page-major';
      major.textContent = heading.textContent.trim();
      group.appendChild(major);
      var subs = document.createElement('div');
      subs.className = 'atlas-chapter-page-subs';
      group.appendChild(subs);
      fragment.appendChild(group);
      records.push({ id: heading.id, group: group, link: major });
      links[heading.id] = major;
    } else {
      var sub = document.createElement('a');
      sub.href = '#' + heading.id;
      sub.className = 'atlas-chapter-page-sub';
      sub.textContent = heading.textContent.trim();
      group.lastChild.appendChild(sub);
      links[heading.id] = sub;
    }
  });
  list.replaceChildren(fragment);
  var activeId = '';
  function locate() {
    var header = document.querySelector('.site-header');
    var offset = (header ? header.getBoundingClientRect().height : 55) + 48;
    var active = headings[0];
    headings.forEach(function (h) {
      if (h.getBoundingClientRect().top <= offset) active = h;
    });
    if (!active) return;
    var majorId = records[0].id;
    headings.some(function (h) {
      if (h.tagName === 'H2') majorId = h.id;
      return h === active;
    });
    if (activeId === active.id) return;
    activeId = active.id;
    records.forEach(function (r) {r.group.classList.toggle('is-current', r.id === majorId);});
    Object.keys(links).forEach(function (id) {
      if (id === activeId) links[id].setAttribute('aria-current','location');
      else links[id].removeAttribute('aria-current');
    });
  }
  var pending = false;
  function update() {if (!pending) {pending = true;requestAnimationFrame(function () {pending = false;locate();});}}
  window.addEventListener('scroll',update,{passive:true});
  window.addEventListener('resize',update);
  window.addEventListener('hashchange',function () {requestAnimationFrame(locate);});
  list.addEventListener('click',function (event) {
    var a = event.target.closest('a[href^="#"]');
    if (a) {var id = a.getAttribute('href').slice(1);if (links[id]) {
      activeId = '';
      var hit = headings.find(function (h) {return h.id === id;});
      if (hit) requestAnimationFrame(function () {hit.scrollIntoView({block:'start'});requestAnimationFrame(locate);});
    }}
  });
  locate();
})();

/* PFM-LEFT-CHAPTER-CATALOG-FIX-2026-10-30: independent, responsive left chapter navigation. */
(function () {
  'use strict';
  var match = /^\/chapters\/([A-Z][A-Z0-9]*)\.html$/i.exec(location.pathname);
  if (!match) return;
  var chapterId = match[1].toUpperCase();
  // The left catalogue must not depend on whether the right-hand outline was initialized.
  function init() {
    if (!document.querySelector('main .doc article.prose')) return;
    var left = document.querySelector('.atlas-chapter-catalog-float');
    if (!left) {
      var chapters = [{"label":"Preparation","items":[["P0","Preparation overview"],["P1","Budget Call"],["P2","Citizen engagement"],["P3","Regional Development Council consultations"],["P4","Program convergence"],["P5","Agency Tier 1 proposals: ongoing expenditures"],["P6","Tier 1 deliberations"],["P7","Budget Priorities Framework"],["P8","Agency Tier 2 proposals: new or expanded spending"],["P9","Tier 2 deliberations"],["P10","Presentation to the President and Cabinet"],["P11","Confirmation and finalization"],["P12","The President's Budget submitted to Congress"]]},{"label":"Legislation","items":[["L0","Legislation overview"],["L1","House deliberations"],["L2","Senate deliberations"],["L3","Bicameral deliberations"],["L4","Ratification and enrolment"],["L5","Enactment of the General Appropriations Act"]]},{"label":"Execution","items":[["E0","Execution overview"],["E1","Early procurement activities"],["E2","Budget execution program"],["E3","Allotment release"],["E4","Obligation"],["E5","Cash allocation"],["E6","Disbursement"]]},{"label":"Accountability","items":[["A0","Accountability overview"],["A1","Performance targets"],["A2","Citizen engagement"],["A3","Monitoring and evaluation"],["A4","Agencies' accountability reports"],["A5","Performance review"],["A6","In-year reports"],["A7","DBCC Mid-Year Report"],["A8","DBCC Year-End Report"],["A9","Audit report"]]},{"label":"Shared chapters","items":[["IS","Information systems and IFMIS"],["UACS","UACS and record identifiers"]]}];
      left = document.createElement('nav');
      left.className = 'atlas-chapter-catalog-float';
      left.setAttribute('aria-label', 'All chapters');
      var heading = document.createElement('div');
      heading.className = 'atlas-chapter-catalog-head';
      heading.textContent = 'ALL CHAPTERS';
      left.appendChild(heading);
      var toggle = document.createElement('button');
      toggle.className = 'atlas-chapter-catalog-toggle';
      toggle.type = 'button';
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Browse all chapters');
      left.appendChild(toggle);
      var list = document.createElement('div');
      list.className = 'atlas-chapter-catalog-list';
      chapters.forEach(function (phase) {
        var group = document.createElement('section');
        group.className = 'atlas-chapter-catalog-group';
        var label = document.createElement('p');
        label.className = 'atlas-chapter-catalog-phase';
        label.textContent = phase.label;
        group.appendChild(label);
        phase.items.forEach(function (item) {
          var a = document.createElement('a');
          a.href = item[0] + '.html';
          var code = document.createElement('span');
          code.className = 'atlas-chapter-catalog-id';
          code.textContent = item[0];
          var text = document.createElement('span');
          text.className = 'atlas-chapter-catalog-name';
          text.textContent = item[1];
          a.appendChild(code);
          a.appendChild(text);
          if (item[0] === chapterId) a.setAttribute('aria-current', 'page');
          group.appendChild(a);
        });
        list.appendChild(group);
      });
      left.appendChild(list);
      document.body.appendChild(left);
      function close() { left.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); }
      toggle.addEventListener('click', function () {
        var open = !left.classList.contains('is-open');
        left.classList.toggle('is-open', open);
        toggle.setAttribute('aria-expanded', String(open));
      });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
      document.addEventListener('click', function (e) { if (!left.contains(e.target)) close(); });
      list.addEventListener('click', function (e) { if (e.target.closest('a')) close(); });
    }
    document.body.classList.add('atlas-dual-chapter-nav');
    var button = left.querySelector('.atlas-chapter-catalog-toggle');
    if (button) button.textContent = 'Chapters (' + chapterId + ')';
    var current = left.querySelector('a[aria-current="page"]');
    var list = left.querySelector('.atlas-chapter-catalog-list');
    if (current && list) requestAnimationFrame(function () {
      list.scrollTop = Math.max(0, current.offsetTop - list.offsetTop - list.clientHeight / 3);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();

/* PFM-CHAPTER-CATALOG-WIDTH-INDEX-2026-10-30: chapter index uses the same left rail. */
(function () {
  'use strict';
  if (!/\/chapters\/index\.html$/i.test(window.location.pathname)) return;
  function init() {
    if (document.querySelector('.atlas-chapter-catalog-float')) return;
    var phases = [{"label":"Preparation","items":[["P0","Preparation overview"],["P1","Budget Call"],["P2","Citizen engagement"],["P3","Regional Development Council consultations"],["P4","Program convergence"],["P5","Agency Tier 1 proposals: ongoing expenditures"],["P6","Tier 1 deliberations"],["P7","Budget Priorities Framework"],["P8","Agency Tier 2 proposals: new or expanded spending"],["P9","Tier 2 deliberations"],["P10","Presentation to the President and Cabinet"],["P11","Confirmation and finalization"],["P12","The President's Budget submitted to Congress"]]},{"label":"Legislation","items":[["L0","Legislation overview"],["L1","House deliberations"],["L2","Senate deliberations"],["L3","Bicameral deliberations"],["L4","Ratification and enrolment"],["L5","Enactment of the General Appropriations Act"]]},{"label":"Execution","items":[["E0","Execution overview"],["E1","Early procurement activities"],["E2","Budget execution program"],["E3","Allotment release"],["E4","Obligation"],["E5","Cash allocation"],["E6","Disbursement"]]},{"label":"Accountability","items":[["A0","Accountability overview"],["A1","Performance targets"],["A2","Citizen engagement"],["A3","Monitoring and evaluation"],["A4","Agencies' accountability reports"],["A5","Performance review"],["A6","In-year reports"],["A7","DBCC Mid-Year Report"],["A8","DBCC Year-End Report"],["A9","Audit report"]]},{"label":"Shared chapters","items":[["IS","Information systems and IFMIS"],["UACS","UACS and record identifiers"]]}];
    var nav = document.createElement('nav');
    nav.className = 'atlas-chapter-catalog-float';
    nav.setAttribute('aria-label', 'All chapters');
    var heading = document.createElement('div');
    heading.className = 'atlas-chapter-catalog-head';
    heading.textContent = 'ALL CHAPTERS';
    nav.appendChild(heading);
    var button = document.createElement('button');
    button.className = 'atlas-chapter-catalog-toggle';
    button.type = 'button';
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-label', 'Browse all chapters');
    button.textContent = 'All chapters';
    nav.appendChild(button);
    var list = document.createElement('div');
    list.className = 'atlas-chapter-catalog-list';
    phases.forEach(function (phase) {
      var section = document.createElement('section');
      section.className = 'atlas-chapter-catalog-group';
      var label = document.createElement('p');
      label.className = 'atlas-chapter-catalog-phase';
      label.textContent = phase.label;
      section.appendChild(label);
      phase.items.forEach(function (item) {
        var link = document.createElement('a');
        link.href = item[0] + '.html';
        var id = document.createElement('span');
        id.className = 'atlas-chapter-catalog-id';
        id.textContent = item[0];
        var name = document.createElement('span');
        name.className = 'atlas-chapter-catalog-name';
        name.textContent = item[1];
        link.appendChild(id);
        link.appendChild(name);
        section.appendChild(link);
      });
      list.appendChild(section);
    });
    nav.appendChild(list);
    document.body.appendChild(nav);
    // Reuse the proven responsive dual-chapter CSS; do not change the right-hand panel.
    document.body.classList.add('atlas-dual-chapter-nav');
    function close() {
      nav.classList.remove('is-open');
      button.setAttribute('aria-expanded', 'false');
    }
    button.addEventListener('click', function () {
      var open = !nav.classList.contains('is-open');
      nav.classList.toggle('is-open', open);
      button.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('keydown', function (event) { if (event.key === 'Escape') close(); });
    document.addEventListener('click', function (event) { if (!nav.contains(event.target)) close(); });
    list.addEventListener('click', function (event) { if (event.target.closest('a')) close(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();

/* PFM-REFERENCE-LEFT-NAV-TABLES-2026-10-30: reference catalogue and table sizing. */
(function () {
  'use strict';
  var match = /\/reference\/(index|[a-g])\.html$/i.exec(window.location.pathname);
  if (!match) return;
  var activeId = match[1].toLowerCase();
  if (document.querySelector('.atlas-reference-float')) return;

  document.body.classList.add('atlas-reference-nav');
  var entries = [
    ['a', 'Authorities and mandates'],
    ['b', 'Information systems'],
    ['c', 'Documents and identifiers'],
    ['d', 'Legal framework'],
    ['e', 'Glossary and abbreviations'],
    ['f', 'Sources and verification'],
    ['g', 'Open questions and gaps']
  ];
  var rail = document.createElement('nav');
  rail.className = 'atlas-reference-float';
  rail.setAttribute('aria-label', 'All references');
  var head = document.createElement('div');
  head.className = 'atlas-reference-float-head';
  head.textContent = 'ALL REFERENCES';
  rail.appendChild(head);
  var toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = 'atlas-reference-float-toggle';
  toggle.textContent = 'All references';
  toggle.setAttribute('aria-expanded', 'false');
  toggle.setAttribute('aria-controls', 'atlas-reference-float-links');
  rail.appendChild(toggle);
  var links = document.createElement('div');
  links.className = 'atlas-reference-float-links';
  links.id = 'atlas-reference-float-links';
  function makeLink(id, title) {
    var a = document.createElement('a');
    a.href = id + '.html';
    var badge = document.createElement('span');
    badge.className = 'atlas-reference-float-code';
    badge.textContent = id === 'index' ? 'ALL' : id.toUpperCase();
    var name = document.createElement('span');
    name.textContent = title;
    a.appendChild(badge);
    a.appendChild(name);
    if (activeId === id) a.setAttribute('aria-current', 'page');
    return a;
  }
  links.appendChild(makeLink('index', 'Reference index'));
  entries.forEach(function (entry) { links.appendChild(makeLink(entry[0], entry[1])); });
  rail.appendChild(links);
  document.body.appendChild(rail);
  function close() {
    rail.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  }
  toggle.addEventListener('click', function () {
    var opened = !rail.classList.contains('is-open');
    rail.classList.toggle('is-open', opened);
    toggle.setAttribute('aria-expanded', String(opened));
  });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') close();
  });
  document.addEventListener('click', function (event) {
    if (!rail.contains(event.target)) close();
  });
  links.addEventListener('click', function (event) {
    if (event.target.closest('a')) close();
  });

  // Only reference tables receive fixed, readable column geometry.
  document.querySelectorAll('main .table-wrap > table').forEach(function (table) {
    var headers = Array.prototype.map.call(table.querySelectorAll('thead tr:first-child th'), function (h) {
      return h.textContent.trim().toLowerCase();
    });
    if (!headers.length) return;
    table.classList.add('atlas-ref-table');
    var n = Math.min(9, headers.length);
    table.classList.add('atlas-ref-cols-' + n);
    if (headers.indexOf('role in pfm') !== -1) table.classList.add('atlas-ref-role-table');
    if (headers.indexOf('code') !== -1 && headers.indexOf('source') !== -1) {
      table.classList.add('atlas-ref-source-table');
    }
  });
})();

/* PFM-REFERENCE-TABLE-READABILITY-V2-20261030: content-first, reversible table presentation. */
(function () {
  'use strict';
  if (!/\/reference\/(?:index|[a-g])\.html$/i.test(window.location.pathname)) return;
  function ready() {
    var tables = Array.prototype.slice.call(document.querySelectorAll('main .table-wrap > table'));
    if (!tables.length) return;
    document.body.classList.add('atlas-ref-tables-v2');
    var focused = null;
    var lastFocus = null;
    function closeWide() {
      if (!focused) return;
      var frame = focused;
      focused = null;
      frame.classList.remove('is-wide');
      document.body.classList.remove('atlas-ref-wide-open');
      frame.querySelector('.atlas-ref-wide-button').textContent = 'Full-width table';
      if (lastFocus && document.contains(lastFocus)) lastFocus.focus();
      lastFocus = null;
      if (frame._refLayout) frame._refLayout();
    }
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && focused) {
        event.preventDefault();
        closeWide();
      }
    });
    function columnSpec(label) {
      var h = label.toLowerCase().replace(/\s+/g, ' ').trim();
      if (/^(no\.|no|code|mark|abbreviation|total|read\?|kind of key)$/.test(h)) return [4.5, 0];
      if (/^(chapters|chapters affected|basis|where it shows)$/.test(h)) return [9, .4];
      if (/^(kind|carrier|stage of use|state|status in the sources|lead|owner)$/.test(h)) return [9, .6];
      if (/^(from|to|from record|to record|where|sections|provision|law|document|record|term|authority|party|system|issuance|bill|decision|subject|source|fact|column)$/.test(h)) return [13, 1];
      if (/^(role in pfm|what it holds or does|what the atlas does|what it does|what it proves|what it does not prove|what it governs|what passes|how i read it|how it was read|what would settle it|what is missing in a row|effect on the atlas|least certain part|used for|rule|meaning|content|reason|plan|check of both sides|question|values)$/.test(h)) return [23, 3];
      if (/^(text a|text b|source a|source b|recipient \(reads data\)|user \(enters data\)|do not confuse with|identified by|why it matters|where to check|open point|issued or prepared by|systems it owns|linking key|field read on a form or in a rule\?)$/.test(h)) return [17, 2];
      if (/^(spending side|revenue and treasury side|inside one agency|how it was read|g o v e r n s|defect|full name|usual time of issue)$/.test(h)) return [14, 1];
      return [15, 1.2];
    }
    tables.forEach(function (table, index) {
      var headers = Array.prototype.map.call(table.querySelectorAll('thead tr:first-child th'), function (th) {
        return th.textContent.trim();
      });
      if (!headers.length) return;
      var wrap = table.parentElement;
      var frame = document.createElement('div');
      frame.className = 'atlas-ref-table-frame';
      wrap.parentNode.insertBefore(frame, wrap);
      var toolbar = document.createElement('div');
      toolbar.className = 'atlas-ref-table-toolbar';
      var caption = document.createElement('span');
      caption.className = 'atlas-ref-table-caption';
      var rows = Array.prototype.slice.call(table.querySelectorAll('tbody > tr'));
      caption.textContent = 'Table ' + (index + 1) + ' · ' + rows.length + ' records';
      toolbar.appendChild(caption);
      var mode = document.createElement('div');
      mode.className = 'atlas-ref-table-actions';
      var asRecords = document.createElement('button');
      asRecords.type = 'button'; asRecords.textContent = 'Read as records';
      asRecords.setAttribute('aria-pressed', 'false');
      var asTable = document.createElement('button');
      asTable.type = 'button'; asTable.textContent = 'Table';
      asTable.setAttribute('aria-pressed', 'true');
      var wide = document.createElement('button');
      wide.type = 'button'; wide.className = 'atlas-ref-wide-button'; wide.textContent = 'Full-width table';
      mode.appendChild(asRecords); mode.appendChild(asTable); mode.appendChild(wide);
      toolbar.appendChild(mode);
      var hint = document.createElement('div');
      hint.className = 'atlas-ref-table-hint';
      hint.textContent = 'More columns available: scroll horizontally or open the full-width table.';
      frame.appendChild(toolbar);
      frame.appendChild(hint);
      frame.appendChild(wrap);
      table.classList.add('atlas-ref-v2-table');
      var specs = headers.map(columnSpec);
      var colgroup = document.createElement('colgroup');
      specs.forEach(function () { colgroup.appendChild(document.createElement('col')); });
      table.insertBefore(colgroup, table.firstChild);
      var records = null;
      var cards = null;
      function buildRecords() {
        if (records) return;
        records = document.createElement('div');
        records.className = 'atlas-ref-records';
        var numberHeader = /^(no\.|no|code)$/i.test(headers[0]);
        rows.forEach(function (tr, i) {
          var cells = Array.prototype.slice.call(tr.children).filter(function (cell) {
            return cell.tagName === 'TD' || cell.tagName === 'TH';
          });
          if (!cells.length) return;
          var article = document.createElement('article');
          article.className = 'atlas-ref-record';
          if (tr.id) article.setAttribute('data-row-id', tr.id);
          if (tr.hasAttribute('data-status')) article.setAttribute('data-status', tr.getAttribute('data-status'));
          var head = document.createElement('div');
          head.className = 'atlas-ref-record-head';
          var tag = document.createElement('span'); tag.className = 'atlas-ref-record-tag';
          var idLink = numberHeader ? cells[0].querySelector('a.row-id') : null;
          tag.textContent = numberHeader ? (idLink ? idLink.textContent.trim() : cells[0].textContent.trim().split(/\s+/)[0]) : String(i + 1).padStart(2, '0');
          head.appendChild(tag);
          var statusDot = cells[0].querySelector('.status-dot[title]');
          if (statusDot) {
            var status = document.createElement('span');
            status.className = 'atlas-ref-record-status';
            status.textContent = statusDot.getAttribute('title');
            head.appendChild(status);
          }
          var title = document.createElement('strong');
          var mainCell = cells[numberHeader && cells.length > 1 ? 1 : 0];
          if (mainCell.textContent.trim()) {
            Array.prototype.forEach.call(mainCell.childNodes, function (node) {
              var copy = node.cloneNode(true);
              if (copy.nodeType === 1) {
                if (copy.hasAttribute('id')) copy.removeAttribute('id');
                Array.prototype.forEach.call(copy.querySelectorAll('[id]'), function (child) {child.removeAttribute('id');});
              }
              title.appendChild(copy);
            });
          } else title.textContent = 'Record ' + (i + 1);
          head.appendChild(title);
          article.appendChild(head);
          var dl = document.createElement('dl');
          dl.className = 'atlas-ref-record-fields';
          cells.forEach(function (cell, c) {
            if (c >= headers.length || c === 0 || (numberHeader && c === 1)) return;
            if (!cell.textContent.trim()) return;
            var entry = document.createElement('div');
            entry.className = 'atlas-ref-record-field';
            if (cell.textContent.trim().length > 130) entry.classList.add('is-long');
            var dt = document.createElement('dt'); dt.textContent = headers[c] || ('Column ' + (c + 1));
            var dd = document.createElement('dd');
            Array.prototype.forEach.call(cell.childNodes, function (node) {
              var copy = node.cloneNode(true);
              if (copy.nodeType === 1) {
                if (copy.hasAttribute('id')) copy.removeAttribute('id');
                Array.prototype.forEach.call(copy.querySelectorAll('[id]'), function (child) {child.removeAttribute('id');});
              }
              dd.appendChild(copy);
            });
            entry.appendChild(dt); entry.appendChild(dd); dl.appendChild(entry);
          });
          article.appendChild(dl);
          records.appendChild(article);
          if (!cards) cards = [];
          cards.push({tr:tr, article:article});
        });
        frame.appendChild(records);
        function syncHidden() {
          cards.forEach(function (pair) {
            pair.article.hidden = pair.tr.hidden || pair.tr.style.display === 'none';
          });
        }
        syncHidden();
        if (cards.some(function (pair) {return pair.tr.hasAttribute('data-status');})) {
          var observer = new MutationObserver(syncHidden);
          observer.observe(table, {attributes:true, subtree:true, attributeFilter:['hidden','style']});
          frame._refObserver = observer;
        }
      }
      function layout() {
        if (wrap.hidden) return;
        var rem = parseFloat(window.getComputedStyle(document.documentElement).fontSize) || 16;
        var available = Math.max(0, wrap.clientWidth - 4);
        var widths = specs.map(function (spec) {return spec[0] * rem;});
        var minimum = widths.reduce(function (sum,x) {return sum + x;},0);
        var spare = Math.max(0, available - minimum);
        var weightSum = specs.reduce(function (sum,spec) {return sum + spec[1];},0);
        if (weightSum > 0 && spare) widths.forEach(function (width,j) {widths[j] += spare * specs[j][1] / weightSum;});
        var total = Math.max(minimum, available);
        Array.prototype.forEach.call(colgroup.children, function (col,j) {col.style.width = Math.ceil(widths[j]) + 'px';});
        table.style.setProperty('width', Math.ceil(total) + 'px', 'important');
        var overflow = total > available + 6;
        frame.classList.toggle('has-horizontal-overflow', overflow);
      }
      frame._refLayout = layout;
      function findDeepLink() {
        if (!window.location.hash || !cards) return;
        var hash = decodeURIComponent(window.location.hash.slice(1));
        var match = cards.filter(function (pair) {return pair.tr.id === hash && !pair.article.hidden;})[0];
        if (match && frame.classList.contains('is-record-mode')) {
          requestAnimationFrame(function () {match.article.scrollIntoView({block:'start'});});
        }
      }
      window.addEventListener('hashchange', findDeepLink);
      function setMode(recordMode) {
        if (focused) closeWide();
        if (recordMode) buildRecords();
        wrap.hidden = recordMode;
        if (records) records.hidden = !recordMode;
        frame.classList.toggle('is-record-mode', recordMode);
        asRecords.setAttribute('aria-pressed', String(recordMode));
        asTable.setAttribute('aria-pressed', String(!recordMode));
        if (!recordMode) requestAnimationFrame(layout);
        else findDeepLink();
      }
      asRecords.addEventListener('click', function () {setMode(true);});
      asTable.addEventListener('click', function () {setMode(false);});
      wide.addEventListener('click', function () {
        if (focused === frame) {closeWide();return;}
        if (focused) closeWide();
        if (wrap.hidden) setMode(false);
        focused = frame;
        lastFocus = wide;
        frame.classList.add('is-wide');
        document.body.classList.add('atlas-ref-wide-open');
        wide.textContent = 'Close wide view';
        requestAnimationFrame(layout);
        wide.focus();
      });
      var lenMax = 0;
      rows.slice(0, 25).forEach(function (tr) {
        Array.prototype.forEach.call(tr.children, function (td) {
          lenMax = Math.max(lenMax, (td.textContent || '').trim().length);
        });
      });
      var defaultRecords = (headers.length >= 5 && lenMax > 150) || (headers.length === 4 && lenMax > 450);
      setMode(defaultRecords);
      if (window.ResizeObserver) new ResizeObserver(layout).observe(wrap);
      window.addEventListener('resize', layout);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready, {once:true});
  else ready();
})();


/* PFM-DIAGRAM-CATALOG-V1: use the existing chapter-width left rail on diagram pages. */
(function () {
  'use strict';
  var nav = document.querySelector('.atlas-diagram-catalog-float');
  if (!nav) return;
  var toggle = nav.querySelector('.atlas-chapter-catalog-toggle');
  var links = nav.querySelector('.atlas-chapter-catalog-list');
  var query = nav.querySelector('.atlas-diagram-catalog-search');
  var phases = Array.prototype.slice.call(nav.querySelectorAll('.atlas-diagram-phase'));
  var chapters = Array.prototype.slice.call(nav.querySelectorAll('.atlas-diagram-chapter'));
  // Remember initial expansion states so a search can restore the normal outline.
  function close() {
    nav.classList.remove('is-open');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
  }
  if (toggle) toggle.addEventListener('click', function () {
    var expanded = !nav.classList.contains('is-open');
    nav.classList.toggle('is-open', expanded);
    toggle.setAttribute('aria-expanded', String(expanded));
  });
  if (links) links.addEventListener('click', function (event) {
    if (event.target.closest('a')) close();
  });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') close();
  });
  document.addEventListener('click', function (event) {
    if (!nav.contains(event.target)) close();
  });
  if (query) {
    var wasOpen = null;
    query.addEventListener('input', function () {
      var needle = query.value.trim().toLocaleLowerCase();
      if (needle && !wasOpen) wasOpen = new Map(phases.concat(chapters).map(function (d) {return [d, d.open];}));
      nav.classList.toggle('is-filtering', !!needle);
      chapters.forEach(function (chapter) {
        var found = 0;
        chapter.querySelectorAll('.atlas-diagram-catalog-link').forEach(function (a) {
          var ok = !needle || (a.textContent + ' ' + a.title).toLocaleLowerCase().indexOf(needle) !== -1;
          a.hidden = !ok;
          if (ok) found += 1;
        });
        chapter.hidden = Boolean(needle) && !found;
        if (needle && found) chapter.open = true;
      });
      phases.forEach(function (phase) {
        var has = Array.prototype.some.call(phase.querySelectorAll('.atlas-diagram-chapter'), function (c) {
          return !c.hidden;
        });
        phase.hidden = Boolean(needle) && !has;
        if (needle && has) phase.open = true;
      });
      if (!needle && wasOpen) {
        wasOpen.forEach(function (open, d) {d.open = open;});
        wasOpen = null;
      }
    });
  }
  // Bring the active diagram into view without moving the article itself.
  var current = nav.querySelector('.atlas-diagram-catalog-link[aria-current="page"]');
  if (current && links) requestAnimationFrame(function () {
    links.scrollTop = Math.max(0, current.offsetTop - links.offsetTop - links.clientHeight / 3);
  });
})();
