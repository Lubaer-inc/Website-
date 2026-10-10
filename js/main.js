(() => {
  const gallery = document.getElementById("gallery");
  const filters = document.querySelector(".filters");
  const lightbox = document.getElementById("lightbox");
  const lbMedia = lightbox.querySelector(".lb-media");
  const lbCaption = lightbox.querySelector("figcaption");
  let visible = WERKE;
  let current = 0;

  const caption = (w) => [w.titel, w.jahr, w.technik, w.masse].filter(Boolean).join(", ");

  function media(w, large) {
    if (w.bild) {
      const img = document.createElement("img");
      img.src = w.bild;
      img.alt = caption(w);
      if (!large) img.loading = "lazy";
      return img;
    }
    const ph = document.createElement("div");
    ph.className = "placeholder";
    ph.style.background = w.farbe || "#ccc";
    ph.setAttribute("role", "img");
    ph.setAttribute("aria-label", caption(w));
    return ph;
  }

  function renderGallery() {
    gallery.replaceChildren(
      ...visible.map((w, i) => {
        const li = document.createElement("li");
        const btn = document.createElement("button");
        btn.className = "work";
        btn.append(media(w, false));
        const cap = document.createElement("span");
        cap.className = "work-caption";
        cap.innerHTML = `<strong></strong> <span></span>`;
        cap.firstChild.textContent = w.titel;
        cap.lastChild.textContent = w.jahr;
        btn.append(cap);
        btn.addEventListener("click", () => open(i));
        li.append(btn);
        return li;
      })
    );
  }

  function renderFilters() {
    const cats = ["Alle", ...new Set(WERKE.map((w) => w.kategorie).filter(Boolean))];
    if (cats.length < 3) return;
    cats.forEach((c, i) => {
      const b = document.createElement("button");
      b.textContent = c;
      b.setAttribute("aria-pressed", i === 0);
      b.addEventListener("click", () => {
        filters.querySelectorAll("button").forEach((x) => x.setAttribute("aria-pressed", x === b));
        visible = c === "Alle" ? WERKE : WERKE.filter((w) => w.kategorie === c);
        renderGallery();
      });
      filters.append(b);
    });
  }

  function show(i) {
    current = (i + visible.length) % visible.length;
    const w = visible[current];
    lbMedia.replaceChildren(media(w, true));
    lbCaption.textContent = caption(w);
  }

  function open(i) {
    show(i);
    lightbox.showModal();
  }

  lightbox.querySelector(".lb-close").addEventListener("click", () => lightbox.close());
  lightbox.querySelector(".lb-prev").addEventListener("click", () => show(current - 1));
  lightbox.querySelector(".lb-next").addEventListener("click", () => show(current + 1));
  lightbox.addEventListener("click", (e) => { if (e.target === lightbox) lightbox.close(); });
  lightbox.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") show(current - 1);
    if (e.key === "ArrowRight") show(current + 1);
  });

  const exList = document.getElementById("exhibitions");
  AUSSTELLUNGEN.forEach((a) => {
    const li = document.createElement("li");
    const year = document.createElement("span");
    year.className = "year";
    year.textContent = a.jahr;
    const body = document.createElement("span");
    const t = document.createElement("strong");
    t.textContent = a.titel;
    body.append(t, document.createTextNode(` – ${a.ort}`));
    const kind = document.createElement("span");
    kind.className = "muted";
    kind.textContent = a.art;
    li.append(year, body, kind);
    exList.append(li);
  });

  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("nav");
  toggle.addEventListener("click", () => {
    const openNav = toggle.getAttribute("aria-expanded") !== "true";
    toggle.setAttribute("aria-expanded", openNav);
    nav.classList.toggle("open", openNav);
  });
  nav.addEventListener("click", (e) => {
    if (e.target.tagName === "A") {
      toggle.setAttribute("aria-expanded", "false");
      nav.classList.remove("open");
    }
  });

  document.getElementById("year").textContent = new Date().getFullYear();
  renderFilters();
  renderGallery();
})();
