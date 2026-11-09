/* Carewise site behaviour: icons, mobile nav, reveal-on-scroll, contact form */
(function () {
  "use strict";

  // Icons
  if (window.lucide) lucide.createIcons();

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
