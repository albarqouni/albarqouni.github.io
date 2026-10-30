// Albarqouni Lab — small, dependency-free helpers shared by all custom layouts.
//   1. Faceted filtering for any [data-filter-root] list (state mirrored in the URL query string)
//   2. Live citation counts from OpenAlex for every [data-doi] element
//   3. The interactive globe on the home page (globe.gl is loaded only there)
(function () {
  "use strict";

  const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);

  // ---------------------------------------------------------------- filters
  document.querySelectorAll("[data-filter-root]").forEach((root) => {
    const items = [...root.querySelectorAll("[data-item]")];
    const controls = [...root.querySelectorAll("[data-facet]")];
    const search = root.querySelector("[data-search]");
    const counters = root.querySelectorAll("[data-count]");
    const groups = [...root.querySelectorAll("[data-group]")];
    const empty = root.querySelector("[data-empty]");

    function apply(push) {
      const q = (search && search.value ? search.value : "").toLowerCase().trim();
      const sel = {};
      controls.forEach((c) => { if (c.value) sel[c.dataset.facet] = c.value; });
      let n = 0;
      items.forEach((it) => {
        let ok = true;
        for (const [f, v] of Object.entries(sel)) {
          const vals = (it.dataset["f" + cap(f)] || "").split("|");
          if (!vals.includes(v)) { ok = false; break; }
        }
        if (ok && q) ok = (it.dataset.text || it.textContent).toLowerCase().includes(q);
        it.hidden = !ok;
        if (ok) n++;
      });
      groups.forEach((g) => { g.hidden = !g.querySelector("[data-item]:not([hidden])"); });
      counters.forEach((c) => { c.textContent = n; });
      if (empty) empty.hidden = n > 0;
      controls.forEach((c) => c.classList.toggle("lab-active", !!c.value));
      if (push !== false) {
        const params = new URLSearchParams();
        Object.entries(sel).forEach(([k, v]) => params.set(k, v));
        if (q) params.set("q", q);
        const qs = params.toString();
        history.replaceState(null, "", qs ? "?" + qs + location.hash : location.pathname + location.hash);
      }
    }

    const initial = new URLSearchParams(location.search);
    controls.forEach((c) => {
      if (initial.get(c.dataset.facet)) c.value = initial.get(c.dataset.facet);
      c.addEventListener("change", apply);
    });
    if (search) {
      search.value = initial.get("q") || "";
      search.addEventListener("input", apply);
    }
    // Clickable chips / bars that set a facet, e.g. <button data-set-facet="year=2024">
    root.querySelectorAll("[data-set-facet]").forEach((b) =>
      b.addEventListener("click", (e) => {
        e.preventDefault();
        const [f, v] = b.dataset.setFacet.split("=");
        const c = controls.find((x) => x.dataset.facet === f);
        if (!c) return;
        c.value = c.value === v ? "" : v;
        apply();
        const list = root.querySelector("[data-list]");
        if (list) list.scrollIntoView({ behavior: "smooth", block: "start" });
      })
    );
    const reset = root.querySelector("[data-reset]");
    if (reset) reset.addEventListener("click", () => {
      controls.forEach((c) => { c.value = ""; });
      if (search) search.value = "";
      apply();
    });
    apply(false);
  });

  // ---------------------------------------------------------- live citations
  const citeEls = [...document.querySelectorAll("[data-doi]")];
  const totalEls = document.querySelectorAll("[data-total-citations]");
  if (citeEls.length && document.documentElement.dataset.labLiveCitations !== "false") {
    const norm = (d) => d.toLowerCase().replace(/^https?:\/\/(dx\.)?doi\.org\//, "").trim();
    const dois = [...new Set(citeEls.map((e) => norm(e.dataset.doi)).filter(Boolean))];
    const counts = {};
    const chunks = [];
    for (let i = 0; i < dois.length; i += 50) chunks.push(dois.slice(i, i + 50));
    Promise.all(
      chunks.map((c) =>
        fetch("https://api.openalex.org/works?per-page=50&select=doi,cited_by_count&filter=doi:" +
              c.map(encodeURIComponent).join("|"))
          .then((r) => (r.ok ? r.json() : { results: [] }))
          .then((j) => (j.results || []).forEach((w) => { if (w.doi) counts[norm(w.doi)] = w.cited_by_count; }))
          .catch(() => {})
      )
    ).then(() => {
      let total = 0;
      citeEls.forEach((el) => {
        const n = counts[norm(el.dataset.doi)];
        if (n === undefined) return;
        const target = el.querySelector("[data-cite-value]") || el;
        target.textContent = n.toLocaleString();
        el.hidden = false;
        el.dataset.citations = n;
        const item = el.closest("[data-item]");
        if (item) item.dataset.citations = n;
      });
      Object.values(counts).forEach((n) => { total += n; });
      totalEls.forEach((el) => {
        const snapshot = parseInt(el.dataset.snapshot || "0", 10);
        // Scholar counts are usually higher than OpenAlex; never show a smaller number than the last Scholar snapshot.
        el.textContent = Math.max(total, snapshot).toLocaleString();
      });
    });
  }

  // ------------------------------------------------------------------ sorting
  document.querySelectorAll("[data-sort]").forEach((sel) => {
    sel.addEventListener("change", () => {
      const root = sel.closest("[data-filter-root]");
      const byCites = sel.value === "citations";
      root.classList.toggle("lab-flat", byCites);
      const flat = root.querySelector("[data-flat-list]");
      const items = [...root.querySelectorAll("[data-item]")];
      if (byCites) {
        items.sort((a, b) => (+b.dataset.citations || 0) - (+a.dataset.citations || 0)).forEach((it) => flat.appendChild(it));
      } else {
        items.forEach((it) => {
          const home = root.querySelector('[data-group="' + it.dataset.home + '"] [data-group-items]');
          if (home) home.appendChild(it);
        });
        root.querySelectorAll("[data-group-items]").forEach((g) =>
          [...g.children].sort((a, b) => (b.dataset.date || "").localeCompare(a.dataset.date || "")).forEach((c) => g.appendChild(c))
        );
      }
    });
  });

  // -------------------------------------------------------------------- banner: pillars + globe
  const globeEl = document.getElementById("lab-globe");
  const dataEl = document.getElementById("lab-globe-data");
  const banner = document.querySelector("[data-banner]");
  if (banner && dataEl) {
    const data = JSON.parse(dataEl.textContent);
    const home = data.home;
    const tabs = [...banner.querySelectorAll("[data-pillar]")];
    const panels = [...banner.querySelectorAll("[data-pillar-panel]")];
    const legend = banner.querySelector("[data-globe-legend]");
    let globe = null;

    if (globeEl && window.Globe) {
      globe = Globe()(globeEl)
        .backgroundColor("rgba(0,0,0,0)")
        .globeImageUrl((document.documentElement.dataset.hbbRelurl || "/") + "vendor/globe/earth-night.jpg")
        .bumpImageUrl((document.documentElement.dataset.hbbRelurl || "/") + "vendor/globe/earth-topology.png")
        .showAtmosphere(true).atmosphereColor("#2d9d9b").atmosphereAltitude(0.17)
        .pointLat("lat").pointLng("lon")
        .pointAltitude((p) => (p.home ? 0.07 : 0.025))
        .pointRadius((p) => (p.home ? 0.55 : 0.32))
        .pointColor((p) => p.color)
        .pointLabel((p) => '<div class="lab-globe-tip"><b>' + p.name + "</b></div>")
        .onPointClick((p) => { if (p.url) window.open(p.url, "_blank", "noopener"); })
        .arcStartLat("a_lat").arcStartLng("a_lon").arcEndLat("b_lat").arcEndLng("b_lon")
        .arcColor((a) => a.colors).arcStroke(0.5)
        .arcDashLength(0.5).arcDashGap(0.25).arcDashAnimateTime(2400)
        .ringsData([home]).ringLat("lat").ringLng("lon")
        .ringColor(() => (t) => "rgba(252,186,0," + (1 - t) + ")")
        .ringMaxRadius(5).ringPropagationSpeed(2).ringRepeatPeriod(1400);
      globe.pointOfView({ lat: 32, lng: 18, altitude: 2.1 }, 0);
      const controls = globe.controls();
      controls.autoRotate = !matchMedia("(prefers-reduced-motion: reduce)").matches;
      controls.autoRotateSpeed = 0.4;
      controls.enableZoom = false;
      const resize = () => { globe.width(globeEl.clientWidth); globe.height(globeEl.clientHeight); };
      resize();
      // re-measure whenever the box changes (fonts, CSS and images can settle after the globe is created)
      if (window.ResizeObserver) new ResizeObserver(resize).observe(globeEl);
      else addEventListener("resize", resize);
    }

    const far = (p) => Math.abs(p.lat - home.lat) + Math.abs(p.lon - home.lon) > 0.6;
    function show(i) {
      const t = data.tabs[i];
      tabs.forEach((b, k) => b.setAttribute("aria-selected", k === i ? "true" : "false"));
      panels.forEach((p, k) => { p.hidden = k !== i; });
      if (legend) legend.innerHTML = '<i style="background:' + t.color + '"></i>' + t.label +
        (t.inflows.length ? ' &nbsp; <i style="background:#2d9d9b"></i>' + t.inflow_label : "");
      if (!globe) return;
      const tint = t.color === "#173869" || t.color === "#3c3489" || t.color === "#5f6670" ? "#5cc6c3" : t.color;
      const pts = [{ ...home, home: true, color: "#ffffff" }].concat(t.pins.map((p) => ({ ...p, color: tint })));
      const arcs = t.pins.filter(far).map((p) => ({ a_lat: home.lat, a_lon: home.lon, b_lat: p.lat, b_lon: p.lon, colors: ["#ffffff", tint] }))
        .concat(t.inflows.map((ll) => ({ a_lat: ll[1], a_lon: ll[0], b_lat: home.lat, b_lon: home.lon, colors: ["#2d9d9b", "#ffffff"] })));
      globe.pointsData(pts).arcsData(arcs);
      const inEurope = t.pins.length && t.pins.every((p) => p.lat > 35 && p.lat < 60 && p.lon > -10 && p.lon < 30);
      globe.pointOfView(inEurope ? { lat: 46, lng: 12, altitude: 1.55 } : { lat: 28, lng: 22, altitude: 2.05 }, 1200);
    }

    // auto-cycle through pillars until the visitor interacts
    let cur = 0;
    let timer = null;
    const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
    const stop = () => { if (timer) clearInterval(timer); timer = null; };
    tabs.forEach((b, k) => b.addEventListener("click", () => { stop(); cur = k; show(k); }));
    [globeEl, ...panels].forEach((el) => el && el.addEventListener("pointerdown", stop, { once: true }));
    show(0);
    if (!reduce && tabs.length > 1) {
      timer = setInterval(() => {
        if (document.hidden) return;
        cur = (cur + 1) % tabs.length;
        show(cur);
      }, 7000);
    }
  }
})();

// ---------------------------------------------------------- application form
// Sends the form to Web3Forms, which emails it to the PI. Nothing is stored by this site.
document.querySelectorAll("[data-lab-form]").forEach((form) => {
  const status = form.querySelector("[data-form-status]");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const fd = new FormData(form);
    const data = {};
    for (const [k, v] of fd.entries()) data[k] = data[k] ? data[k] + ", " + v : v;
    data.subject = form.dataset.subject.replace(/\{(\w+)\}/g, (_, k) => data[k] || "");
    data.replyto = data.email;
    const btn = form.querySelector("[type=submit]");
    btn.disabled = true;
    status.textContent = "Sending…";
    try {
      const res = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data),
      });
      const json = await res.json();
      if (!json.success) throw new Error(json.message || "failed");
      form.reset();
      form.innerHTML = '<p class="lab-success">' + form.dataset.success + "</p>";
    } catch (err) {
      status.textContent = "Sorry, sending failed (" + err.message + "). Please try again or email us directly.";
      btn.disabled = false;
    }
  });
});

// ---------------------------------------------------------- before/after slider ({{< compare >}} shortcode)
document.querySelectorAll("[data-compare]").forEach((fig) => {
  const stage = fig.querySelector(".lab-compare-stage");
  const range = fig.querySelector(".lab-compare-range");
  const set = (v) => {
    v = Math.max(0, Math.min(100, v));
    stage.style.setProperty("--pos", v + "%");
    range.value = v;
  };
  const fromX = (x) => {
    const r = stage.getBoundingClientRect();
    return ((x - r.left) / r.width) * 100;
  };
  let drag = false;
  stage.addEventListener("pointerdown", (e) => { drag = true; stage.setPointerCapture(e.pointerId); set(fromX(e.clientX)); });
  stage.addEventListener("pointermove", (e) => drag && set(fromX(e.clientX)));
  stage.addEventListener("pointerup", () => (drag = false));
  stage.addEventListener("pointercancel", () => (drag = false));
  range.addEventListener("input", () => set(+range.value));
  fig.querySelectorAll("[data-before-src]").forEach((b) => b.addEventListener("click", () => {
    fig.querySelector("[data-before]").src = b.dataset.beforeSrc;
    fig.querySelector("[data-after]").src = b.dataset.afterSrc;
    fig.querySelectorAll("[data-before-src]").forEach((x) => x.classList.toggle("is-active", x === b));
    set(50);
  }));
});
