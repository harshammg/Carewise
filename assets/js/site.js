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

  // Video testimonials: open in a lightbox and play
  var lb = document.getElementById("vt-lightbox");
  var openers = Array.prototype.slice.call(document.querySelectorAll(".vt-open"));
  if (lb && openers.length) {
    var lbVideo = lb.querySelector(".vt-lb-video");
    var lbName = lb.querySelector(".vt-lb-caption strong");
    var lbRole = lb.querySelector(".vt-lb-caption span");
    var idx = 0, lastFocus = null;
    function show(i) {
      idx = (i + openers.length) % openers.length;
      var b = openers[idx];
      lbVideo.src = b.getAttribute("data-video");
      lbName.textContent = b.getAttribute("data-name") || "";
      lbRole.textContent = b.getAttribute("data-role") || "";
      var p = lbVideo.play();
      if (p && p.catch) p.catch(function () {});
    }
    function open(i, from) {
      lastFocus = from || document.activeElement;
      lb.hidden = false;
      document.body.classList.add("vt-lock");
      requestAnimationFrame(function () { lb.classList.add("is-open"); });
      show(i);
      lb.querySelector(".vt-lb-close").focus();
    }
    function close() {
      lb.classList.remove("is-open");
      lbVideo.pause();
      lbVideo.removeAttribute("src");
      lbVideo.load();
      document.body.classList.remove("vt-lock");
      setTimeout(function () { lb.hidden = true; }, 250);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }
    openers.forEach(function (b, i) {
      b.addEventListener("click", function () { open(i, b); });
    });
    lb.querySelector(".vt-lb-close").addEventListener("click", close);
    lb.querySelector(".vt-lb-prev").addEventListener("click", function () { show(idx - 1); });
    lb.querySelector(".vt-lb-next").addEventListener("click", function () { show(idx + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    lbVideo.addEventListener("ended", function () { show(idx + 1); });
    document.addEventListener("keydown", function (e) {
      if (lb.hidden) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowRight") show(idx + 1);
      else if (e.key === "ArrowLeft") show(idx - 1);
    });
  }

  // Image lightbox for photo tiles (each grid is its own prev/next group)
  var ilb = document.getElementById("img-lightbox");
  if (ilb && document.querySelector(".img-open")) {
    var ilbImg = ilb.querySelector(".img-lb-img");
    var ilbCap = ilb.querySelector(".img-lb-caption");
    var group = [], gi = 0, ilbFocus = null;
    function ishow(i) {
      gi = (i + group.length) % group.length;
      var b = group[gi];
      ilbImg.src = b.getAttribute("data-src");
      ilbImg.alt = b.getAttribute("data-caption") || "";
      ilbCap.textContent = b.getAttribute("data-caption") || "";
    }
    function iopen(btn) {
      var host = btn.closest(".fac-grid") || document;
      group = Array.prototype.slice.call(host.querySelectorAll(".img-open"));
      ilbFocus = btn;
      ilb.hidden = false;
      document.body.classList.add("vt-lock");
      requestAnimationFrame(function () { ilb.classList.add("is-open"); });
      ishow(group.indexOf(btn));
      ilb.querySelector(".vt-lb-close").focus();
    }
    function iclose() {
      ilb.classList.remove("is-open");
      document.body.classList.remove("vt-lock");
      setTimeout(function () { ilb.hidden = true; ilbImg.removeAttribute("src"); }, 250);
      if (ilbFocus && ilbFocus.focus) ilbFocus.focus();
    }
    document.querySelectorAll(".img-open").forEach(function (b) {
      b.addEventListener("click", function () { iopen(b); });
    });
    ilb.querySelector(".vt-lb-close").addEventListener("click", iclose);
    ilb.querySelector(".vt-lb-prev").addEventListener("click", function () { ishow(gi - 1); });
    ilb.querySelector(".vt-lb-next").addEventListener("click", function () { ishow(gi + 1); });
    ilb.addEventListener("click", function (e) { if (e.target === ilb) iclose(); });
    document.addEventListener("keydown", function (e) {
      if (ilb.hidden) return;
      if (e.key === "Escape") iclose();
      else if (e.key === "ArrowRight") ishow(gi + 1);
      else if (e.key === "ArrowLeft") ishow(gi - 1);
    });
  }

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
      var url = "https://wa.me/917619457863?text=" + encodeURIComponent(lines.join("\n"));
      window.open(url, "_blank", "noopener");
      var note = form.querySelector(".form-note");
      if (note) note.textContent = "Opening WhatsApp with your message. If it did not open, call +91 76194 57863.";
    });
  }
})();
