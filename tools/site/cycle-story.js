/* Philippine PFM Atlas: the budget-cycle story and the step explorer of the home page.
   Presentation only. The data and the text come from tools/budget_cycle_story.py through the page.
   Without JavaScript the page shows the text of the story and every step panel; this file adds the drawing that
   changes with the story, and the selection, colour and search of the explorer.
   Colours come from the tokens of style.css, so the light and dark themes of the site apply. */
(function () {
  "use strict";
  var story = document.getElementById("cycle-story");
  var dataEl = document.getElementById("cs-data");
  if (!story || !dataEl) return;
  var D;
  try { D = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var NS = "http://www.w3.org/2000/svg";
  var RM = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };
  var S = D.steps, BY = {};
  S.forEach(function (s, i) { s.i = i; BY[s.id] = s; });
  var LY = { authority: .16, claim: .40, cash: .64, records: .86 };
  var LINES = [["authority", "Legal authority"], ["claim", "The claim"], ["cash", "Cash"], ["records", "Records and control"]];

  function el(t, a, p) { var e = document.createElementNS(NS, t); for (var k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; }
  function tw(t) { try { return t.getComputedTextLength(); } catch (e) { return 60; } }

  /* ---------- drawing ---------- */
  var fig = story.querySelector(".cs-fig"), svg = story.querySelector(".cs-svg"), ov = story.querySelector(".cs-ov"), cap = story.querySelector(".cs-cap");
  story.classList.add("cs-live");
  function grp(cls, hidden) { var g = el("g", { "class": "cs-grp " + cls }, svg); if (hidden) g.style.opacity = 0; return g; }
  var gAxis = grp("cs-axis", 1), gGhost = grp("cs-ghosts", 1), gLines = grp("cs-lines", 1), gMp = grp("cs-mps", 1),
      gNodes = grp("cs-nodes"), gIns = grp("cs-inss", 1), gArcs = grp("cs-arcs"), gTok = grp("cs-toks", 1), gDate = grp("cs-date", 1);
  var dl = el("line", {}, gDate), dt = el("text", {}, gDate);

  S.forEach(function (s) {
    var g = el("g", { "class": "cs-node ph-" + s.ph }, gNodes);
    s.g = g; s.rect = el("rect", {}, g);
    s.tid = el("text", { "class": "cs-nid" }, g); s.tid.textContent = s.id;
    s.tlb = el("text", { "class": "cs-nlb" }, g); s.t1 = el("tspan", {}, s.tlb); s.t2 = el("tspan", {}, s.tlb);
    s.cur = { x: 0, y: 0, w: 0, h: 0, rx: 6, ix: 0, iy: 0, lx: 0, ly: 0 }; s.tgt = Object.assign({}, s.cur);
    s.g25 = el("rect", { "class": "cs-ghost ph-" + s.ph }, gGhost); s.g27 = el("rect", { "class": "cs-ghost ph-" + s.ph }, gGhost);
  });
  var ins = D.inserted.map(function (a) {
    var g = el("g", { "class": "cs-ins" }, gIns); var c = el("circle", { r: 6 }, g); c.style.stroke = "var(--" + a[2] + ")";
    var t = el("text", {}, g); return { a: a, g: g, c: c, t: t };
  });
  var tracks = LINES.map(function (x) {
    var l = el("line", { "class": "cs-track cs-tr-" + x[0] }, gLines); var t = el("text", { "class": "cs-lname" }, gLines);
    t.textContent = x[1]; t.style.fill = "var(--" + x[0] + ")"; return { k: x[0], l: l, t: t };
  });
  var lapse = el("line", { "class": "cs-lapse" }, gLines); lapse.style.opacity = 0;
  var mps = [["authority", "claim", .47, 1], ["authority", "claim", .74, 2], ["claim", "cash", .84, 3]].map(function (a) {
    var g = el("g", { "class": "cs-mp" }, gMp); var l = el("line", {}, g); var c = el("circle", { r: 10 }, g);
    var t = el("text", { "text-anchor": "middle", "dominant-baseline": "central" }, g); t.textContent = a[3];
    return { a: a, g: g, l: l, c: c, t: t };
  });
  var toks = ["authority", "claim", "cash", "records"].map(function (k) {
    var g = el("g", { "class": "cs-tok" }, gTok); var c = el("circle", { r: 8 }, g); c.style.fill = "var(--" + k + ")";
    g.style.opacity = 0; return { k: k, g: g, c: c, cur: 0, tgt: 0, from: 0 };
  });
  var dates = [el("text", { "class": "cs-datelbl" }, gTok), el("text", { "class": "cs-datelbl" }, gTok)];
  var paid = el("text", { "class": "cs-paid" }, gTok); paid.textContent = "Paid";
  dates.forEach(function (d) { d.style.opacity = 0; }); paid.style.opacity = 0;

  var W = 600, H = 800, compact = false, scene = null, geo = {};
  function measure() {
    var wf = document.querySelector(".atlas-page-wayfinder");
    story.style.setProperty("--cs-top", (document.querySelector(".site-header")?.offsetHeight || (wf ? wf.offsetHeight : 0)) + "px");
    var r = svg.getBoundingClientRect(); W = Math.max(280, r.width); H = Math.max(260, r.height);
    svg.setAttribute("viewBox", "0 0 " + W + " " + H); compact = W < 560 || H < 520; svg.classList.toggle("cs-compact", compact);
  }

  function setLoop() {
    var p = 6, cw = (W - 2 * p) / 5, ch = (H - 2 * p) / 13, gap = compact ? 3 : 5;
    geo.loop = { p: p, cw: cw, ch: ch, cx: p + cw, cy: p + ch, cW: 3 * cw, cH: 11 * ch };
    S.forEach(function (s) {
      var x = p + (s.pos[0] - 1) * cw + gap / 2, y = p + (s.pos[1] - 1) * ch + gap / 2, w = cw - gap, h = ch - gap, t = s.tgt;
      t.x = x; t.y = y; t.w = w; t.h = h; t.rx = compact ? 4 : 6;
      if (compact) { s.t1.textContent = ""; s.t2.textContent = ""; t.ix = x + w / 2 - tw(s.tid) / 2; t.iy = y + h / 2 + 4; t.lx = x + 6; t.ly = y + h / 2; }
      else { s.t1.textContent = s.short[0]; s.t2.textContent = s.short[1] || ""; t.ix = x + 7; t.iy = y + 13; t.lx = x + 7; t.ly = y + (s.short[1] ? Math.min(h - 17, 29) : Math.min(h - 6, 30)); }
    });
    var L = geo.loop;
    ov.style.left = (L.cx + L.cw * .12) + "px"; ov.style.top = (L.cy + L.ch * .4) + "px";
    ov.style.width = (L.cW - L.cw * .24) + "px"; ov.style.height = (L.cH - L.ch * .8) + "px";
  }
  function setTime(slice) {
    var top = 34, bot = 26, LW = compact ? 30 : Math.min(W * .4, 262), x0 = LW + 6, x1 = W - 6, rh = (H - top - bot) / 32;
    function tx(m) { return x0 + (Math.max(0, Math.min(36, m)) / 36) * (x1 - x0); }
    geo.time = { top: top, rh: rh, tx: tx };
    S.forEach(function (s) {
      var y = top + s.i * rh, a = slice ? s.calendar[0] : 12 + s.r[0], b = slice ? s.calendar[1] : 12 + s.r[1], t = s.tgt;
      t.x = tx(a); t.w = Math.max(3, tx(b) - tx(a)); t.y = y + rh * .2; t.h = Math.max(3, rh * .6); t.rx = Math.min(3, rh * .3);
      s.t1.textContent = compact ? "" : s.short.join(" "); s.t2.textContent = ""; t.ix = 2; t.iy = y + rh / 2 + 3.5; t.lx = 36; t.ly = y + rh / 2 + 3.5;
      [[s.g25, 0], [s.g27, 24]].forEach(function (pair) {
        var g = pair[0], A = s.r[0] + pair[1], B = s.r[1] + pair[1], vis = B > 0 && A < 36;
        g.setAttribute("x", tx(A)); g.setAttribute("width", vis ? Math.max(0, tx(B) - tx(A)) : 0);
        g.setAttribute("y", y + rh * .2); g.setAttribute("height", Math.max(3, rh * .6)); g.setAttribute("rx", Math.min(3, rh * .3));
        g.dataset.a = A; g.dataset.b = B;
      });
    });
    while (gAxis.firstChild) gAxis.removeChild(gAxis.firstChild);
    ["2025", "2026", "2027"].forEach(function (yr, k) {
      var xa = tx(k * 12), xb = tx(k * 12 + 12);
      if (k === 1) el("rect", { "class": "cs-band", x: xa, y: top - 6, width: xb - xa, height: H - top - bot + 6 }, gAxis);
      el("text", { "class": "cs-yr", x: xa + 4, y: 14 }, gAxis).textContent = yr;
      for (var q = 0; q < 4; q++) {
        var xm = tx(k * 12 + q * 3); el("line", { "class": "cs-tick", x1: xm, x2: xm, y1: top - 8, y2: top - 3 }, gAxis);
        if (!compact || q === 0) el("text", { x: xm + 2, y: 27 }, gAxis).textContent = ["Jan", "Apr", "Jul", "Oct"][q];
      }
    });
  }
  function setLines() {
    var x0 = compact ? 10 : 18, x1 = W - (compact ? 10 : 18), top = 10, hh = H - top - 6;
    function px(f) { return x0 + f * (x1 - x0); }
    function py(k) { return top + LY[k] * hh; }
    geo.lines = { px: px, py: py };
    tracks.forEach(function (t) {
      t.l.setAttribute("x1", x0); t.l.setAttribute("x2", x1); t.l.setAttribute("y1", py(t.k)); t.l.setAttribute("y2", py(t.k));
      t.t.setAttribute("x", x0); t.t.setAttribute("y", py(t.k) - (compact ? 28 : 34));
    });
    function lab(text, f, k, side) { var w = tw(text), x = Math.max(2, Math.min(W - w - 2, px(f) - w / 2)); return [x, side === "up" ? py(k) - 13 : py(k) + (compact ? 20 : 23)]; }
    S.forEach(function (s) {
      var t = s.tgt, m = s.line;
      if (!m) { t.x = s.cur.x; t.y = s.cur.y; return; }
      var cx = px(m[1]), cy = py(m[0]), r = compact ? 6 : 8;
      t.x = cx - r; t.y = cy - r; t.w = 2 * r; t.h = 2 * r; t.rx = r;
      s.t1.textContent = compact ? m[4] : m[3]; s.t2.textContent = "";
      var l = lab(s.tlb, m[1], m[0], m[2]); t.lx = l[0]; t.ly = l[1]; t.ix = cx; t.iy = cy;
    });
    ins.forEach(function (o) {
      var a = o.a; o.c.setAttribute("cx", px(a[3])); o.c.setAttribute("cy", py(a[2])); o.c.setAttribute("r", compact ? 5 : 6);
      o.t.textContent = compact ? a[1] : a[0]; var l = lab(o.t, a[3], a[2], a[4]); o.t.setAttribute("x", l[0]); o.t.setAttribute("y", l[1]);
    });
    mps.forEach(function (m) {
      var x = px(m.a[2]), ya = py(m.a[0]) + 9, yb = py(m.a[1]) - 9;
      m.l.setAttribute("x1", x); m.l.setAttribute("x2", x); m.l.setAttribute("y1", ya); m.l.setAttribute("y2", yb);
      m.c.setAttribute("cx", x + 15); m.c.setAttribute("cy", (ya + yb) / 2); m.t.setAttribute("x", x + 15); m.t.setAttribute("y", (ya + yb) / 2);
    });
    lapse.setAttribute("x1", px(.555)); lapse.setAttribute("x2", px(.815)); lapse.setAttribute("y1", py("cash")); lapse.setAttribute("y2", py("cash"));
    toks.forEach(function (t) { t.c.setAttribute("cy", py(t.k)); });
  }

  var anim = null;
  function draw(s) {
    var c = s.cur;
    s.rect.setAttribute("x", c.x); s.rect.setAttribute("y", c.y); s.rect.setAttribute("width", Math.max(0, c.w)); s.rect.setAttribute("height", Math.max(0, c.h));
    s.rect.setAttribute("rx", Math.max(0, Math.min(c.rx, c.w / 2, c.h / 2)));
    s.tid.setAttribute("x", c.ix); s.tid.setAttribute("y", c.iy); s.tlb.setAttribute("x", c.lx); s.tlb.setAttribute("y", c.ly);
    s.t1.setAttribute("x", c.lx); s.t2.setAttribute("x", c.lx); s.t2.setAttribute("dy", s.t2.textContent ? "1.2em" : "0");
  }
  function tween(dur) {
    S.forEach(function (s) { s.from = Object.assign({}, s.cur); }); toks.forEach(function (t) { t.from = t.cur; });
    var t0 = performance.now(), d = RM.matches ? 0 : dur;
    if (anim) cancelAnimationFrame(anim);
    function step(now) {
      var k = d ? Math.min(1, (now - t0) / d) : 1, e = k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
      S.forEach(function (s) { for (var p in s.tgt) s.cur[p] = s.from[p] + (s.tgt[p] - s.from[p]) * e; draw(s); });
      toks.forEach(function (t) { t.cur = t.from + (t.tgt - t.from) * e; t.c.setAttribute("cx", t.cur); });
      anim = k < 1 ? requestAnimationFrame(step) : null;
    }
    anim = requestAnimationFrame(step);
  }

  var sweep = null, MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  function setDate(m) {
    var G = geo.time, x = G.tx(m);
    dl.setAttribute("x1", x); dl.setAttribute("x2", x); dl.setAttribute("y1", G.top - 6); dl.setAttribute("y2", H - 22);
    var mi = Math.floor(m - 12), day = Math.max(1, Math.round((m - Math.floor(m)) * 30));
    var lbl = day + " " + MON[Math.min(11, mi)] + " 2026"; dt.textContent = lbl;
    var w = tw(dt); dt.setAttribute("x", Math.min(W - w - 2, Math.max(2, x - w / 2))); dt.setAttribute("y", H - 8);
    var c = { 25: 0, 26: 0, 27: 0 }, slice = D.threeView === "slice";
    S.forEach(function (s) {
      [25, 26, 27].forEach(function (fy) { var o = 12 * (fy - 25); if (m >= o + s.r[0] && m < o + s.r[1]) c[fy]++; });
      var a = slice ? s.calendar[0] : 12 + s.r[0], b = slice ? s.calendar[1] : 12 + s.r[1], on = m >= a && m < b;
      s.g.style.opacity = on ? 1 : (slice ? .18 : .28);
      if (!slice) [[s.g25, 25], [s.g27, 27]].forEach(function (pair) { var g = pair[0], o = m >= +g.dataset.a && m < +g.dataset.b; g.style.opacity = o ? .9 : .22; });
    });
    cap.innerHTML = '<span class="cs-k"><b>' + lbl + '</b></span><span class="cs-k"><i class="cs-sw cs-sw-fy25"></i>FY 2025: ' + c[25] +
      ' steps</span><span class="cs-k"><i class="cs-sw cs-sw-fy26"></i>FY 2026: ' + c[26] + '</span><span class="cs-k"><i class="cs-sw cs-sw-fy27"></i>FY 2027: ' + c[27] + '</span>';
  }
  function stopSweep() { if (sweep) cancelAnimationFrame(sweep); sweep = null; }
  function startSweep() {
    stopSweep(); if (RM.matches) { setDate(17.5); return; }
    var t0 = performance.now();
    function f(now) { setDate(12 + ((now - t0) / 1000 * .9) % 12); sweep = requestAnimationFrame(f); }
    sweep = requestAnimationFrame(f);
  }

  function anchor(id) {
    var s = BY[id], c = s.pos[0], r = s.pos[1], t = s.tgt;
    if (r === 1 && c === 1) return [t.x + t.w, t.y + t.h]; if (r === 1 && c === 5) return [t.x, t.y + t.h];
    if (r === 13 && c === 1) return [t.x + t.w, t.y]; if (r === 13 && c === 5) return [t.x, t.y];
    if (r === 1) return [t.x + t.w / 2, t.y + t.h]; if (r === 13) return [t.x + t.w / 2, t.y];
    if (c === 1) return [t.x + t.w, t.y + t.h / 2]; return [t.x, t.y + t.h / 2];
  }
  function drawArcs(list) {
    while (gArcs.firstChild) gArcs.removeChild(gArcs.firstChild);
    if (!list) return;
    var L = geo.loop, cx = L.cx + L.cW / 2, cy = L.cy + L.cH / 2, seen = {};
    list.forEach(function (a, i) {
      var p1 = anchor(a[0]), p2 = anchor(a[1]), mx = (p1[0] + p2[0]) / 2, my = (p1[1] + p2[1]) / 2, qx = mx + (cx - mx) * .55, qy = my + (cy - my) * .55;
      var p = el("path", { "class": "cs-arc" + (a[3] ? " cs-gk" : ""), d: "M" + p1[0] + " " + p1[1] + " Q" + qx + " " + qy + " " + p2[0] + " " + p2[1], "marker-end": "url(#cs-ah)" }, gArcs);
      if (!a[3] && !RM.matches) {
        var len = p.getTotalLength(); p.style.strokeDasharray = len; p.style.strokeDashoffset = len;
        p.style.transition = "stroke-dashoffset 1s ease " + (i * .22) + "s";
        requestAnimationFrame(function () { requestAnimationFrame(function () { p.style.strokeDashoffset = 0; }); });
      }
      if (!seen[a[2]]) {
        seen[a[2]] = 1; var bx = .25 * p1[0] + .5 * qx + .25 * p2[0], by = .25 * p1[1] + .5 * qy + .25 * p2[1];
        var g = el("g", { "class": "cs-arcb" + (a[3] ? " cs-gk" : "") }, gArcs); el("circle", { cx: bx, cy: by, r: compact ? 8 : 10 }, g);
        el("text", { x: bx, y: by, "text-anchor": "middle", "dominant-baseline": "central" }, g).textContent = a[2];
      }
    });
  }

  var PHCAP = '<span class="cs-k"><i class="cs-sw" style="background:var(--cs-prep)"></i>Preparation</span><span class="cs-k"><i class="cs-sw" style="background:var(--cs-leg)"></i>Legislation</span>' +
    '<span class="cs-k"><i class="cs-sw" style="background:var(--cs-exec)"></i>Execution</span><span class="cs-k"><i class="cs-sw" style="background:var(--cs-acc)"></i>Accountability</span>';
  var LNCAP = '<span class="cs-k"><i class="cs-sw" style="background:var(--authority)"></i>Legal authority</span><span class="cs-k"><i class="cs-sw" style="background:var(--claim)"></i>The claim</span>' +
    '<span class="cs-k"><i class="cs-sw" style="background:var(--cash)"></i>Cash</span><span class="cs-k"><i class="cs-sw" style="background:var(--records)"></i>Records and control</span>' +
    '<span class="cs-k"><b>Bold</b>: steps of the loop</span><span class="cs-k"><i>Italic</i>: steps the loop does not draw</span>';
  var TOK = {
    lines: { show: [] },
    mp1: { show: ["authority", "claim", "records"], x: { authority: .47, claim: .47, records: .47 }, mp: ["on", "off", "off"] },
    mp2: { show: ["authority", "claim", "records"], x: { authority: .74, claim: .74, records: .74 }, mp: ["on", "on", "off"] },
    mp3: { show: ["authority", "claim", "cash", "records"], x: { authority: .74, claim: .84, cash: .84, records: .86 }, mp: ["on", "on", "on"], paid: 1 },
    fail: { show: ["authority", "claim", "cash", "records"], x: { authority: .74, claim: .84, cash: .52, records: .74 }, mp: ["on", "on", "wait"], fail: 1 }
  };
  var START = { authority: .10, claim: .16, cash: .20, records: .47 };
  var FOCUS = { prep: "prep", leg: "leg", exec: "exec", acc: "acc" };

  function apply(name, dur) {
    scene = name;
    var lay = (name === "time" || name === "three") ? "time" : (TOK[name] ? "lines" : "loop");
    svg.setAttribute("data-layout", lay); stopSweep();
    S.forEach(function (s) { s.g.classList.remove("ln-authority", "ln-claim", "ln-cash", "ln-records"); });
    var slice = name === "three" && D.threeView === "slice";
    if (lay === "loop") setLoop(); else if (lay === "time") setTime(slice); else setLines();
    var focus = FOCUS[name], arcs = D.arcs[name], inv = {};
    if (arcs) arcs.forEach(function (a) { inv[a[0]] = 1; inv[a[1]] = 1; });
    S.forEach(function (s) {
      var o = 1;
      if (lay === "loop") { if (focus) o = s.ph === focus ? 1 : .18; else if (arcs) o = inv[s.id] ? 1 : .3; }
      else if (lay === "lines") { if (s.line) { s.g.classList.add("ln-" + s.line[0]); } else o = 0; }
      s.g.style.opacity = o;
    });
    gAxis.style.opacity = lay === "time" ? 1 : 0; gGhost.style.opacity = (name === "three" && !slice) ? 1 : 0; gDate.style.opacity = name === "three" ? 1 : 0;
    [gLines, gIns, gMp, gTok].forEach(function (g) { g.style.opacity = lay === "lines" ? 1 : 0; });
    var over = D.overlay[focus || name];
    ov.style.opacity = over && lay === "loop" ? 1 : 0; if (over) ov.innerHTML = over;
    if (lay === "lines") {
      var T = TOK[name], G = geo.lines;
      toks.forEach(function (t) {
        var on = T.show.indexOf(t.k) >= 0;
        if (!on || t.g.style.opacity === "0") { t.cur = G.px(START[t.k]); t.c.setAttribute("cx", t.cur); }
        t.tgt = on ? G.px(T.x[t.k]) : t.cur;
        t.g.style.opacity = on ? ((name === "mp3" && t.k === "authority") ? .45 : (name === "fail" && t.k === "cash") ? .5 : 1) : 0;
      });
      mps.forEach(function (m, i) { m.g.classList.remove("on", "wait"); var st = (T.mp || ["off", "off", "off"])[i]; if (st !== "off") m.g.classList.add(st); });
      paid.style.opacity = T.paid ? 1 : 0;
      var pw = tw(paid); paid.setAttribute("x", G.px(.84) - pw - (compact ? 9 : 13)); paid.setAttribute("y", G.py("cash") - (compact ? 10 : 13));
      lapse.style.opacity = T.fail ? 1 : 0;
      dates[0].textContent = compact ? "30 Jun: NCA lapses" : "30 Jun: unused Q2 NCA lapses";
      dates[1].textContent = compact ? "2 Jul: DV arrives" : "2 Jul: voucher arrives";
      if (T.fail) {
        var w0 = tw(dates[0]), w1 = tw(dates[1]);
        dates[0].setAttribute("x", Math.max(2, Math.min(W - w0 - 2, G.px(.685) - w0 / 2))); dates[0].setAttribute("y", G.py("cash") + (compact ? 36 : 44));
        dates[1].setAttribute("x", W - w1 - 4); dates[1].setAttribute("y", G.py("claim") - (compact ? 27 : 31));
      }
      dates.forEach(function (d) { d.style.opacity = T.fail ? 1 : 0; });
    }
    if (lay === "loop" && arcs) { setTimeout(function () { if (scene === name) drawArcs(arcs); }, RM.matches ? 0 : (dur || 0) * .6); } else drawArcs(null);
    if (name === "time") { S.forEach(function (s) { s.g.style.opacity = 1; }); cap.innerHTML = PHCAP + '<span class="cs-k">Bars: the FY 2026 budget</span>'; }
    else if (name === "three") startSweep();
    else cap.innerHTML = lay === "lines" ? LNCAP : PHCAP;
    tween(dur);
  }

  var steps = Array.prototype.slice.call(story.querySelectorAll(".cs-step"));
  function pick() {
    var desk = window.innerWidth > 820, th = desk ? innerHeight * .55 : innerHeight * .8, a = steps[0];
    steps.forEach(function (s) { if (s.getBoundingClientRect().top < th) a = s; });
    steps.forEach(function (s) { s.classList.toggle("cs-on", s === a); });
    var n = a.getAttribute("data-scene"); if (n !== scene) apply(n, 900);
  }
  var tick = false;
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) stopSweep(); else if (scene === "three") startSweep();
  });
  window.addEventListener("scroll", function () { if (!tick) { tick = true; requestAnimationFrame(function () { tick = false; pick(); }); } }, { passive: true });
  var rz;
  window.addEventListener("resize", function () { clearTimeout(rz); rz = setTimeout(function () { measure(); var n = scene; scene = null; apply(n || "hero", 0); }, 120); });

  measure(); setLoop(); S.forEach(function (s) { s.cur = Object.assign({}, s.tgt); draw(s); });
  if (!RM.matches) {
    S.forEach(function (s, i) { s.g.style.opacity = 0; s.g.style.transitionDelay = (i * .028) + "s"; });
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      S.forEach(function (s) { s.g.style.opacity = 1; });
      setTimeout(function () { S.forEach(function (s) { s.g.style.transitionDelay = ""; }); }, 1500);
    }); });
  }
  scene = "hero"; ov.innerHTML = D.overlay.hero; ov.style.opacity = 1; cap.innerHTML = PHCAP;
  steps[0].classList.add("cs-on"); pick();

  /* ---------- explorer ---------- */
  var ex = document.getElementById("cycle-explorer");
  if (!ex) return;
  ex.classList.add("cs-live");
  var grid = ex.querySelector(".cs-grid"), panels = {}, cells = {}, lastHash = null;
  Array.prototype.forEach.call(ex.querySelectorAll(".cs-panel"), function (p) { panels[p.getAttribute("data-step")] = p; });
  Array.prototype.forEach.call(ex.querySelectorAll(".cs-cell"), function (c) { cells[c.getAttribute("data-step")] = c; });
  function select(id, opts) {
    if (!panels[id]) return;
    var s = BY[id], from = S.filter(function (x) { return x.to.indexOf(id) >= 0; }).map(function (x) { return x.id; });
    S.forEach(function (x) {
      var c = cells[x.id]; c.classList.toggle("cs-sel", x.id === id); c.classList.toggle("cs-to", s.to.indexOf(x.id) >= 0);
      c.classList.toggle("cs-from", from.indexOf(x.id) >= 0); c.setAttribute("aria-current", x.id === id ? "true" : "false");
      c.setAttribute("aria-expanded", x.id === id ? "true" : "false");
      panels[x.id].hidden = x.id !== id;
    });
    if (opts && opts.hash && window.history && history.pushState && location.hash !== "#step-" + id) {
      history.pushState(null, "", "#step-" + id); lastHash = location.hash;
    }
    if (opts && opts.focus) {
      var panel = panels[id]; panel.setAttribute("tabindex", "-1"); panel.focus({ preventScroll: true });
      if (window.innerWidth <= 820) panel.scrollIntoView({ block: "start", behavior: RM.matches ? "auto" : "smooth" });
    }
  }
  ex.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a[data-step]") : null;
    if (!a || !ex.contains(a)) return;
    e.preventDefault(); select(a.getAttribute("data-step"), { hash: true, focus: true });
  });
  var legend = ex.querySelector(".cs-legend");
  function colour(fy) {
    grid.classList.toggle("cs-byfy", fy);
    Array.prototype.forEach.call(ex.querySelectorAll("[data-colour]"), function (b) { b.setAttribute("aria-pressed", String((b.getAttribute("data-colour") === "fy") === fy)); });
    legend.innerHTML = fy
      ? '<span><i class="cs-sw cs-sw-fy25"></i>FY 2025 (closing)</span><span><i class="cs-sw cs-sw-fy26"></i>FY 2026 (in execution)</span><span><i class="cs-sw cs-sw-fy27"></i>FY 2027 (in preparation)</span>'
      : '<span><i class="cs-sw" style="background:var(--cs-prep)"></i>Preparation</span><span><i class="cs-sw" style="background:var(--cs-leg)"></i>Legislation</span><span><i class="cs-sw" style="background:var(--cs-exec)"></i>Execution</span><span><i class="cs-sw" style="background:var(--cs-acc)"></i>Accountability</span>';
  }
  Array.prototype.forEach.call(ex.querySelectorAll("[data-colour]"), function (b) { b.addEventListener("click", function () { colour(b.getAttribute("data-colour") === "fy"); }); });
  var q = document.getElementById("cs-q"), hint = ex.querySelector(".cs-hint");
  function find() {
    var v = q.value.trim().toLowerCase();
    if (!v) { grid.classList.remove("cs-searching"); S.forEach(function (s) { cells[s.id].classList.remove("cs-hit"); }); hint.textContent = ""; return; }
    var n = 0, first = null;
    S.forEach(function (s) { var hit = panels[s.id].getAttribute("data-search").indexOf(v) >= 0; cells[s.id].classList.toggle("cs-hit", hit); if (hit) { n++; if (!first) first = s.id; } });
    grid.classList.add("cs-searching");
    hint.textContent = n ? n + (n === 1 ? " step mentions it" : " steps mention it") : "No step names this document";
    if (first) select(first);
  }
  q.addEventListener("input", find);
  colour(false);
  function fromHash() {
    if (location.hash === lastHash) return !!lastHash;
    lastHash = location.hash;
    var m = /^#step-([PLEA]\d{1,2})$/.exec(location.hash);
    if (m && panels[m[1]]) {
      select(m[1]);
      var target = window.innerWidth <= 820 ? panels[m[1]] : ex;
      requestAnimationFrame(function () { requestAnimationFrame(function () { target.scrollIntoView(); }); });
      return true;
    }
    return false;
  }
  if (!fromHash()) select("P1");
  else window.addEventListener("load", function () { if (/^#step-/.test(location.hash)) ex.scrollIntoView(); });
  window.addEventListener("hashchange", fromHash);
  window.addEventListener("popstate", fromHash);
  /* The four-phase overview uses native disclosures. Wayfinder and deep links open the named phase. */
  function revealPhase() {
    var match = /^#phase-(preparation|legislation|execution|accountability)$/.exec(location.hash);
    if (!match) return;
    var target = document.getElementById("phase-" + match[1]);
    if (target) target.open = true;
  }
  Array.prototype.forEach.call(document.querySelectorAll('a[href^="#phase-"]'), function (link) {
    link.addEventListener("click", function () {
      var target = document.getElementById(link.getAttribute("href").slice(1));
      if (target) target.open = true;
    });
  });
  revealPhase();
  window.addEventListener("hashchange", revealPhase);
})();
