/* Carewise motion: curtain, progress bar, word reveal, counters, tilt, magnetic buttons, spotlight */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) return;

  var body = document.body;

  // Page curtain + progress bar + spotlight layers
  var curtain = document.createElement("div");
  curtain.className = "curtain";
  body.appendChild(curtain);
  function dropCurtain() {
    if (curtain.parentNode) curtain.remove();
  }
  curtain.addEventListener("animationend", dropCurtain);
  setTimeout(dropCurtain, 1600); // background tabs pause animations; never leave the page covered

  var bar = document.createElement("div");
  bar.className = "progress";
  body.appendChild(bar);

  var spot = document.createElement("div");
  spot.className = "spot";
  body.appendChild(spot);

  // Blobs behind hero / page-hero / CTA
  document.querySelectorAll(".hero, .page-hero").forEach(function (sec) {
    ["terracotta", "teal", "sand"].forEach(function (c, i) {
      var b = document.createElement("span");
      b.className = "blob blob--" + c;
      var size = 28 + i * 10;
      b.style.width = size + "vw";
      b.style.height = size + "vw";
      b.style.left = [60, -10, 35][i] + "%";
      b.style.top = [-20, 40, 70][i] + "%";
      sec.prepend(b);
    });
  });

  // Split hero headline into words
  var h1 = document.querySelector(".hero h1");
  if (h1) {
    h1.classList.add("words");
    var i = 0;
    function split(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) {
              frag.appendChild(document.createTextNode(" "));
              return;
            }
            var w = document.createElement("span");
            w.className = "w";
            var inner = document.createElement("span");
            inner.textContent = part;
            inner.style.setProperty("--i", i++);
            w.appendChild(inner);
            frag.appendChild(w);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1) {
          split(n);
        }
      });
    }
    split(h1);
  }

  // Every section animates on scroll: give each content block a reveal with a
  // direction that varies per section, then stagger siblings.
  var variants = ["up", "left", "right", "zoom", "up", "right", "left"];
  var secs = document.querySelectorAll("main > section, .trust, footer .footer-grid");
  secs.forEach(function (sec, si) {
    var v = variants[si % variants.length];
    sec.setAttribute("data-anim", v);
    var host = sec.querySelector(":scope > .wrap") || sec;
    var kids = Array.prototype.filter.call(host.children, function (el) {
      return !el.classList.contains("blob");
    });
    kids.forEach(function (el, idx) {
      // Grids and lists animate their own children instead of as one block
      if (el.matches(".grid, .steps, .stats, .gallery, .contact-grid, .footer-grid, .split, .trust-wrap")) {
        Array.prototype.forEach.call(el.children, function (c, ci) {
          if (!c.classList.contains("reveal")) c.classList.add("reveal");
          c.setAttribute("data-anim", ci % 2 ? "right" : "left");
          if (el.matches(".grid, .steps, .stats, .gallery")) c.setAttribute("data-anim", ci % 3 === 0 ? "up" : ci % 3 === 1 ? "zoom" : "up");
          c.style.setProperty("--d", ci % 6);
        });
        return;
      }
      if (!el.classList.contains("reveal")) el.classList.add("reveal");
      if (!el.hasAttribute("data-anim")) el.setAttribute("data-anim", v);
      el.style.setProperty("--d", idx % 4);
    });
  });
  // Register any new reveal targets with the observer from site.js
  if (window.observeReveal) {
    document.querySelectorAll(".reveal:not(.in)").forEach(function (el) {
      window.observeReveal(el);
    });
  }
  // Items already in the first viewport appear at once
  document.querySelectorAll(".hero .reveal").forEach(function (el) {
    el.classList.add("in");
  });

  // Parallax on section images (desktop pointer devices)
  var parallax = [];
  document.querySelectorAll(".split img, .quote-band img, .page-hero img, .gallery img").forEach(function (img) {
    var wrap = img.parentElement;
    if (getComputedStyle(wrap).overflow === "visible") {
      wrap.style.overflow = "hidden";
      wrap.style.borderRadius = getComputedStyle(img).borderRadius;
      wrap.style.boxShadow = getComputedStyle(img).boxShadow;
      img.style.boxShadow = "none";
    }
    img.style.willChange = "transform";
    img.style.scale = "1.12";
    parallax.push(img);
  });
  function runParallax() {
    var vh = innerHeight;
    parallax.forEach(function (img) {
      var r = img.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var p = (r.top + r.height / 2 - vh / 2) / vh; // -0.5 .. 0.5
      img.style.translate = "0 " + (p * -40) + "px";
    });
  }

  // Stagger index for reveal children
  document.querySelectorAll(".grid, .steps, .stats, .gallery, .trust .wrap, .contact-list").forEach(function (g) {
    Array.prototype.forEach.call(g.children, function (el, idx) {
      el.style.setProperty("--d", idx % 6);
    });
  });

  // Belt-and-braces reveal: anything whose top is inside the viewport gets shown,
  // even if IntersectionObserver is late (e.g. throttled background tabs).
  function revealVisible() {
    var vh = innerHeight;
    document.querySelectorAll(".reveal:not(.in)").forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < vh * 0.92 && r.bottom > 0) el.classList.add("in");
    });
  }

  // Scroll: progress + header shrink
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.transform = "scaleX(" + (max > 0 ? h.scrollTop / max : 0) + ")";
      body.classList.toggle("scrolled", h.scrollTop > 40);
      runParallax();
      revealVisible();
      ticking = false;
    });
  }
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Count-up stats
  var stats = document.querySelectorAll(".stat");
  if (stats.length && "IntersectionObserver" in window) {
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        sio.unobserve(en.target);
        var b = en.target.querySelector("b");
        var text = b.textContent.trim();
        var m = text.match(/^(\d+)(.*)$/);
        if (!m) {
          en.target.classList.add("counted");
          return;
        }
        var target = parseInt(m[1], 10), suffix = m[2], start = null;
        function step(ts) {
          if (!start) start = ts;
          var p = Math.min((ts - start) / 1400, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          b.textContent = Math.round(target * eased) + suffix;
          if (p < 1) requestAnimationFrame(step);
          else en.target.classList.add("counted");
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    stats.forEach(function (s) { sio.observe(s); });
  }

  // 3D tilt on cards (pointer devices only)
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  if (fine) {
    document.querySelectorAll(".card, .quote-card, .room, .step").forEach(function (el) {
      if (el.closest(".marquee")) return;
      el.classList.add("tilt");
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        el.style.setProperty("--mx", x * 100 + "%");
        el.style.setProperty("--my", y * 100 + "%");
        el.style.transform = "perspective(900px) rotateX(" + ((0.5 - y) * 10) + "deg) rotateY(" + ((x - 0.5) * 12) + "deg) translateY(-4px)";
      });
      el.addEventListener("pointerleave", function () {
        el.style.transform = "";
      });
    });

    // Magnetic buttons
    document.querySelectorAll(".btn").forEach(function (b) {
      if (b.closest(".sticky-bar")) return;
      b.addEventListener("pointermove", function (e) {
        var r = b.getBoundingClientRect();
        var dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
        b.style.transform = "translate(" + dx * 0.18 + "px," + dy * 0.28 + "px)";
      });
      b.addEventListener("pointerleave", function () {
        b.style.transform = "";
      });
    });

    // Spotlight
    addEventListener("pointermove", function (e) {
      spot.style.setProperty("--x", e.clientX + "px");
      spot.style.setProperty("--y", e.clientY + "px");
    }, { passive: true });
  }

  // Ripple on click
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".btn");
    if (!b) return;
    var r = b.getBoundingClientRect();
    var s = document.createElement("span");
    var size = Math.max(r.width, r.height);
    s.className = "ripple";
    s.style.width = s.style.height = size + "px";
    s.style.left = e.clientX - r.left - size / 2 + "px";
    s.style.top = e.clientY - r.top - size / 2 + "px";
    b.appendChild(s);
    s.addEventListener("animationend", function () { s.remove(); });
  });
})();
