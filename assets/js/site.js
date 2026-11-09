/* Carewise site behaviour: icons, mobile nav, reveal-on-scroll, contact form */
(function () {
  "use strict";

  // Icons
  if (window.lucide) lucide.createIcons();

  // Top bar typewriter: types and erases a rotating set of messages
  var note = document.querySelector(".topbar-note[data-type]");
  if (note && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var phrases = [];
    try { phrases = JSON.parse(note.getAttribute("data-type")); } catch (e) {}
    var out = note.querySelector(".type-text");
    if (phrases.length && out) {
      var pi = 0, ci = 0, deleting = false;
      out.textContent = "";
      (function tick() {
        var text = phrases[pi];
        ci += deleting ? -1 : 1;
        out.textContent = text.slice(0, ci);
        var delay = deleting ? 35 : 70;
        if (!deleting && ci === text.length) { delay = 2200; deleting = true; }
        else if (deleting && ci === 0) { deleting = false; pi = (pi + 1) % phrases.length; delay = 400; }
        setTimeout(tick, delay);
      })();
    }
  }

  // Mobile navigation drawer
  var toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  // Reveal on scroll (hidden only once JS runs; everything shows after 2s regardless)
  document.documentElement.classList.add("js");
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.classList.add("in");
            io.unobserve(en.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );
    items.forEach(function (el) {
      io.observe(el);
    });
    window.observeReveal = function (el) {
      io.observe(el);
    };
  } else {
    items.forEach(function (el) {
      el.classList.add("in");
    });
  }

  // Crossfade slideshows
  document.querySelectorAll("[data-slideshow]").forEach(function (box) {
    var imgs = box.querySelectorAll("img");
    var dots = box.querySelectorAll(".slideshow-dots span");
    if (imgs.length < 2) return;
    var i = 0, every = parseInt(box.getAttribute("data-interval"), 10) || 4000;
    box.style.setProperty("--slide-every", every + "ms");
    setInterval(function () {
      if (document.hidden) return;
      var prev = i;
      imgs.forEach(function (im) { im.classList.remove("is-prev"); });
      imgs[prev].classList.remove("is-active");
      imgs[prev].classList.add("is-prev");
      if (dots[prev]) dots[prev].classList.remove("is-active");
      i = (i + 1) % imgs.length;
      imgs[i].classList.add("is-active");
      if (dots[i]) {
        // restart the fill animation on the new dot
        dots[i].classList.remove("is-active");
        void dots[i].offsetWidth;
        dots[i].classList.add("is-active");
      }
    }, every);
  });

  // Collapsible grids: show the first N cards, toggle the rest with View more
  document.querySelectorAll(".grid[data-collapsible]").forEach(function (grid) {
    var n = parseInt(grid.getAttribute("data-collapsible"), 10) || 3;
    var cards = Array.prototype.slice.call(grid.children);
    var btn = grid.parentElement.querySelector(".view-more");
    function apply(open) {
      cards.forEach(function (c, i) {
        c.classList.toggle("is-hidden", !open && i >= n);
        if (open && i >= n) c.classList.add("reveal", "in");
      });
      if (btn) {
        btn.setAttribute("aria-expanded", open ? "true" : "false");
        var label = open ? btn.getAttribute("data-less") : btn.getAttribute("data-more");
        btn.firstChild.textContent = label + " ";
      }
    }
    apply(false);
    if (btn) {
      btn.addEventListener("click", function () {
        var open = btn.getAttribute("aria-expanded") !== "true";
        apply(open);
        if (!open) grid.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    }
  });

  // Instagram strip: load the live feed from /api/instagram (Vercel function).
  // If the function is missing or has no token, the embedded posts stay as fallback.
  var igRow = document.querySelector("[data-ig]");
  if (igRow && window.fetch) {
    var igType = igRow.getAttribute("data-ig-type") || "";
    fetch("/api/instagram?limit=12" + (igType ? "&type=" + igType : ""), { headers: { Accept: "application/json" } })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (!data || !data.items || !data.items.length) return;
        var acct = igRow.getAttribute("data-ig-account");
        var html = data.items.map(function (m) {
          var cap = (m.caption || "").replace(/[<>&"]/g, function (c) {
            return { "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;" }[c];
          });
          var isVideo = m.type === "VIDEO";
          return (
            '<li class="ig-card ig-card--live" data-account="' + acct + '">' +
            '<a href="' + m.url + '" target="_blank" rel="noopener" aria-label="Open Instagram post">' +
            '<img src="' + m.image + '" alt="' + (cap || "Instagram post") + '" loading="lazy" />' +
            (isVideo ? '<span class="ig-badge">' + '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>' : "") +
            '<span class="ig-cap">' + cap + "</span>" +
            "</a></li>"
          );
        }).join("");
        igRow.querySelectorAll('[data-account="' + acct + '"]').forEach(function (el) { el.remove(); });
        igRow.insertAdjacentHTML("afterbegin", html);
        igRow.classList.add("ig-row--live");
        var empty = document.querySelector("[data-ig-empty]");
        if (empty) empty.remove();
      })
      .catch(function () {});
  }
  // Contact form: no backend wired yet, so hand off to WhatsApp with the message pre-filled.
  var form = document.querySelector("form[data-contact]");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      var lines = [
        "Hello Carewise, I would like to discuss care for my parent.",
        "Name: " + (fd.get("name") || "-"),
        "Phone: " + (fd.get("phone") || "-"),
        "Care type: " + (fd.get("care_type") || "-"),
        "Details: " + (fd.get("message") || "-"),
      ];
      var url = "https://wa.me/919606268777?text=" + encodeURIComponent(lines.join("\n"));
      window.open(url, "_blank", "noopener");
      var note = form.querySelector(".form-note");
      if (note) note.textContent = "Opening WhatsApp with your message. If it did not open, call +91 96062 68777.";
    });
  }
})();
