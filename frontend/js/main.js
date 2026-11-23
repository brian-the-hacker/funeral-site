const S = window.SITE;
const el = (tag, attrs = {}, ...kids) => {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) k === "text" ? (n.textContent = v) : n.setAttribute(k, v);
  kids.forEach(k => n.append(k));
  return n;
};

/* ---------- shared header / footer ---------- */
const NAV = [["index.html", "Home"], ["about.html", "About us"], ["services.html", "Services"],
             ["gallery.html", "Gallery"], ["contact.html", "Contact"]];
const here = location.pathname.split("/").pop() || "index.html";

const siteHeader = document.getElementById("site-header");
if (siteHeader) siteHeader.innerHTML = `
  <div class="wrap hdr-in">
    <a class="brand" href="index.html" aria-label="${S.name}, home">
      <img data-img="logo" alt="" height="42"><span>Makueni Pamoja</span>
    </a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="nav" aria-label="Open menu"><i></i><i></i><i></i></button>
    <nav class="nav" id="nav" aria-label="Main">${NAV.map(([h, t]) =>
      `<a href="${h}"${h === here ? ' aria-current="page"' : ""}>${t}</a>`).join("")}
      <a class="nav-call" data-tel href="tel:${S.phoneTel}">Call ${S.phoneDisplay}</a>
    </nav>
  </div>`;
const siteFooter = document.getElementById("site-footer");
if (siteFooter) siteFooter.innerHTML = `
  <div class="wrap">
    <div><strong>${S.name}</strong><p>Preserving dignity, serving with compassion, upholding integrity.</p></div>
    <div><a href="tel:${S.phoneTel}">${S.phoneDisplay}</a>
      <a href="https://wa.me/${S.whatsapp}">WhatsApp us</a>
      <a href="mailto:${S.email}">${S.email}</a><span>${S.address}</span></div>
    <div>${NAV.map(([h, t]) => `<a href="${h}">${t}</a>`).join("")}</div>
    <div class="legal">© ${new Date().getFullYear()} ${S.name}</div>
  </div>`;

/* ---------- images from config ---------- */
document.querySelectorAll("img[data-img]").forEach(i => { if (S.img && S.img[i.dataset.img]) i.src = S.img[i.dataset.img]; });
document.querySelectorAll("[data-bg]").forEach(n => { n.style.backgroundImage = `url("${S.img[n.dataset.bg]}")`; });
document.querySelectorAll("[data-tel]").forEach(a => { a.href = "tel:" + S.phoneTel; });
document.querySelectorAll("[data-wa]").forEach(a => { a.href = "https://wa.me/" + S.whatsapp; });

/* ---------- gallery ---------- */
const thumb = u => u.includes("res.cloudinary.com") ? u.replace("/upload/", "/upload/w_700,f_auto,q_auto/") : u;
const grid = document.getElementById("gallery-grid");
if (grid) {
  const draw = items => {
    grid.replaceChildren(...items.map(it => {
      if (it.resource_type === "video")
        return el("figure", {}, el("video", { src: it.url, controls: "", preload: "none" }));
      const img = el("img", { src: thumb(it.url), alt: it.caption || "Makueni Pamoja Funeral Home", loading: "lazy" });
      return el("figure", {}, el("a", { href: it.url, target: "_blank", rel: "noopener" }, img),
                it.caption ? el("figcaption", { text: it.caption }) : "");
    }));
  };
  fetch(S.api + "/api/gallery")
    .then(r => (r.ok ? r.json() : Promise.reject()))
    .then(items => (items.length ? draw(items) : Promise.reject()))
    .catch(() => draw((S.fallbackGallery || []).map(url => ({ url, resource_type: /\.mp4$/i.test(url) ? "video" : "image" }))));
}

/* ---------- contact form ---------- */
const form = document.getElementById("contact-form");
if (form) {
  const note = document.getElementById("form-note");
  form.addEventListener("submit", async e => {
    e.preventDefault();
    const b = form.querySelector("button");
    b.disabled = true; note.className = ""; note.textContent = "Sending…";
    try {
      const r = await fetch(S.api + "/api/contact", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(new FormData(form)))
      });
      if (!r.ok) throw new Error();
      form.reset(); note.className = "ok";
      note.textContent = "Message sent. We will call or email you back shortly.";
    } catch {
      note.className = "err";
      note.textContent = `Your message was not sent. Please call ${S.phoneDisplay} or message us on WhatsApp.`;
    }
    b.disabled = false;
  });
}

/* ============================================================
   Homepage experience
   ============================================================ */
(() => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const root = document.documentElement;


  /* header: solid after hero start, hides on scroll down, returns on scroll up */
  const hdr = document.getElementById("site-header");
  const inner = document.body.classList.contains("inner");
  if (inner && hdr) hdr.classList.add("solid");
  const burger = document.getElementById("burger");
  const nav = document.getElementById("nav");
  const hero = document.getElementById("heroImg");
  const band = document.getElementById("bandImg");

  const setMenu = open => {
    root.classList.toggle("menu-open", open);
    if (burger) {
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }
    document.body.style.overflow = open ? "hidden" : "";
  };

  if (burger && nav) {
    burger.addEventListener("click", () => setMenu(!root.classList.contains("menu-open")));
    nav.addEventListener("click", e => { if (e.target.closest("a")) setMenu(false); });
    document.addEventListener("keydown", e => {
      if (e.key === "Escape" && root.classList.contains("menu-open")) { setMenu(false); burger.focus(); }
    });
    window.matchMedia("(min-width: 861px)").addEventListener("change", e => { if (e.matches) setMenu(false); });
  }

  let lastY = window.scrollY, ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const y = window.scrollY;
      if (hdr) {
        if (!inner) hdr.classList.toggle("solid", y > 40);
        const goingDown = y > lastY && y > 320;
        hdr.classList.toggle("hide", goingDown && !root.classList.contains("menu-open"));
      }
      lastY = y;

      /* subtle parallax, only while the element is on screen */
      if (!reduce) {
        const vh = window.innerHeight;
        if (hero && y < vh) hero.style.transform = `translate3d(0, ${y * 0.12}px, 0)`;
        if (band) {
          const r = band.parentElement.getBoundingClientRect();
          if (r.bottom > 0 && r.top < vh) {
            const p = (r.top + r.height / 2 - vh / 2) / vh;
            band.style.transform = `translate3d(0, ${p * -60}px, 0)`;
          }
        }
      }
      ticking = false;
    });
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* reveals */
  const targets = document.querySelectorAll(".rv, .wipe");
  if ("IntersectionObserver" in window && !reduce) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -6% 0px" });
    targets.forEach((t, i) => {
      if (t.classList.contains("wipe")) t.style.transitionDelay = (i % 2) * 0.15 + "s";
      io.observe(t);
    });
  } else {
    targets.forEach(t => t.classList.add("in"));
  }

  /* services index: choose a service, the photo changes */
  const list = document.getElementById("svList");
  const view = document.getElementById("svView");
  if (list && view) {
    const items = [...list.querySelectorAll(".sv-item")];
    const imgs = [...view.querySelectorAll("img")];
    const select = i => {
      items.forEach((it, n) => {
        it.classList.toggle("on", n === i);
        it.querySelector(".sv-btn").setAttribute("aria-expanded", String(n === i));
      });
      imgs.forEach((im, n) => im.classList.toggle("on", n === i));
    };
    list.addEventListener("click", e => {
      const b = e.target.closest(".sv-btn");
      if (b) select(Number(b.dataset.i));
    });
    list.addEventListener("mouseover", e => {
      const b = e.target.closest(".sv-btn");
      if (b && window.matchMedia("(hover: hover)").matches) select(Number(b.dataset.i));
    });
    list.addEventListener("focusin", e => {
      const b = e.target.closest(".sv-btn");
      if (b) select(Number(b.dataset.i));
    });
  }
})();
