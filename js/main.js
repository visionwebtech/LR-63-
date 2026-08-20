/* ==========================================================
   LR-63 — main.js
   Preloader particle-logo build, custom cursor, nav, hero
   reveal and GSAP ScrollTrigger scroll system.
   ========================================================== */

(function () {
  "use strict";

  var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var isTouch = window.matchMedia("(hover: none), (pointer: coarse)").matches;
  var isMobile = window.innerWidth <= 860;

  /* ---------------------------------------------------------
     1. PRELOADER — particles converge into the LR-63 logo
  --------------------------------------------------------- */
  function runPreloader(done) {
    var preloader = document.getElementById("preloader");
    var canvas = document.getElementById("preloader-canvas");
    var mark = preloader.querySelector(".preloader-mark");

    if (prefersReduced) {
      // Skip the particle build entirely; just fade the panel out.
      setTimeout(function () {
        preloader.classList.add("is-hidden");
        done();
      }, 350);
      return;
    }

    var ctx = canvas.getContext("2d");
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var size = Math.min(window.innerWidth, window.innerHeight) * 0.55;
    size = Math.max(260, Math.min(size, 460));
    canvas.style.width = size + "px";
    canvas.style.height = size + "px";
    canvas.width = size * dpr;
    canvas.height = size * dpr;
    ctx.scale(dpr, dpr);

    // Load the real logo, sample its bright pixels into a point cloud.
    var img = new Image();
    img.src = "assets/img/lr63-logo.png";
    img.onload = function () {
      var off = document.createElement("canvas");
      off.width = size;
      off.height = size;
      var octx = off.getContext("2d");
      octx.drawImage(img, 0, 0, size, size);
      var data;
      try {
        data = octx.getImageData(0, 0, size, size).data;
      } catch (e) {
        // canvas read blocked (e.g. file:// CORS) — fall back to a plain fade
        startFallback();
        return;
      }

      var points = [];
      var step = Math.max(3, Math.round(size / 130));
      for (var y = 0; y < size; y += step) {
        for (var x = 0; x < size; x += step) {
          var i = (y * size + x) * 4;
          var r = data[i], g = data[i + 1], b = data[i + 2];
          var brightness = (r + g + b) / 3;
          if (brightness > 60) {
            points.push({
              tx: x,
              ty: y,
              x: Math.random() * size,
              y: Math.random() * size,
              vx: 0,
              vy: 0,
              delay: Math.random() * 0.4,
              brightness: brightness
            });
          }
        }
      }

      var start = null;
      var duration = 1500;

      function frame(ts) {
        if (!start) start = ts;
        var elapsed = ts - start;
        var progress = Math.min(1, elapsed / duration);

        ctx.clearRect(0, 0, size, size);
        for (var k = 0; k < points.length; k++) {
          var p = points[k];
          var localT = Math.max(0, Math.min(1, (progress - p.delay) / (1 - p.delay)));
          var eased = 1 - Math.pow(1 - localT, 3);
          var cx = p.x + (p.tx - p.x) * eased;
          var cy = p.y + (p.ty - p.y) * eased;
          var isGold = p.brightness < 210;
          ctx.fillStyle = isGold
            ? "rgba(205,163,95," + (0.35 + eased * 0.65) + ")"
            : "rgba(245,244,239," + (0.35 + eased * 0.65) + ")";
          var r2 = 1.1 + eased * 0.4;
          ctx.beginPath();
          ctx.arc(cx, cy, r2, 0, Math.PI * 2);
          ctx.fill();
        }

        if (progress < 1) {
          requestAnimationFrame(frame);
        } else {
          finishPreloader();
        }
      }
      requestAnimationFrame(frame);
    };

    img.onerror = startFallback;

    function startFallback() {
      // Logo failed to load for pixel sampling — simple gold pulse instead.
      canvas.style.display = "none";
      preloader.style.background = "var(--black)";
      setTimeout(finishPreloader, 900);
    }

    function finishPreloader() {
      if (mark && window.gsap) {
        gsap.to(mark, { opacity: 1, duration: 0.4 });
      } else if (mark) {
        mark.style.opacity = 1;
      }
      setTimeout(function () {
        preloader.classList.add("is-hidden");
        done();
      }, 550);
    }

    // Absolute safety net: never let the preloader block the site.
    setTimeout(function () {
      if (!preloader.classList.contains("is-hidden")) {
        preloader.classList.add("is-hidden");
        done();
      }
    }, 4500);
  }

  /* ---------------------------------------------------------
     2. CUSTOM CURSOR
  --------------------------------------------------------- */
  function initCursor() {
    if (isTouch) return;
    var dot = document.getElementById("cursorDot");
    var ring = document.getElementById("cursorRing");
    var mx = window.innerWidth / 2, my = window.innerHeight / 2;
    var rx = mx, ry = my;

    window.addEventListener("mousemove", function (e) {
      mx = e.clientX;
      my = e.clientY;
      dot.style.transform = "translate(" + mx + "px," + my + "px) translate(-50%,-50%)";
    });

    (function tick() {
      rx += (mx - rx) * 0.16;
      ry += (my - ry) * 0.16;
      ring.style.transform = "translate(" + rx + "px," + ry + "px) translate(-50%,-50%)";
      requestAnimationFrame(tick);
    })();

    var hoverables = document.querySelectorAll("a, button, [data-hover]");
    hoverables.forEach(function (el) {
      el.addEventListener("mouseenter", function () { ring.classList.add("is-hover"); });
      el.addEventListener("mouseleave", function () { ring.classList.remove("is-hover"); });
    });
  }

  /* ---------------------------------------------------------
     3. NAV — scrolled state + mobile menu
  --------------------------------------------------------- */
  function initNav() {
    var nav = document.getElementById("siteNav");
    var toggle = document.getElementById("navToggle");
    var menu = document.getElementById("mobileMenu");

    function onScroll() {
      if (window.scrollY > 40) nav.classList.add("is-scrolled");
      else nav.classList.remove("is-scrolled");
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    toggle.addEventListener("click", function () {
      var open = toggle.classList.toggle("is-open");
      menu.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        toggle.classList.remove("is-open");
        menu.classList.remove("is-open");
      });
    });
  }

  /* ---------------------------------------------------------
     4. HERO REVEAL — masked line reveal + staggered fade
  --------------------------------------------------------- */
  function initHero() {
    if (!window.gsap) return;
    var tl = gsap.timeline({ defaults: { ease: "power3.out" } });
    tl.to(".hero-kicker-logo", { opacity: 1, duration: 0.6 })
      .to(".hero-headline .line span", { y: "0%", duration: 1, stagger: 0.09 }, 0.1)
      .to(".hero-sub", { opacity: 1, duration: 0.8 }, "-=0.5")
      .to(".hero-cta-row", { opacity: 1, duration: 0.8 }, "-=0.6")
      .to(".hero-scroll-cue", { opacity: 1, duration: 0.6 }, "-=0.5")
      .to(".hero-tags", { opacity: 1, duration: 0.6 }, "-=0.5")
      .to(".hero-tags span", { opacity: 1, duration: 0.4, stagger: 0.08 }, "-=0.4");
  }

  /* ---------------------------------------------------------
     5. SCROLL SYSTEM (GSAP ScrollTrigger)
  --------------------------------------------------------- */
  function initScrollSystem() {
    if (!window.gsap || !window.ScrollTrigger || prefersReduced) {
      initSimpleReveals();
      return;
    }
    gsap.registerPlugin(ScrollTrigger);

    /* --- Services: vertical scroll drives horizontal track --- */
    if (!isMobile) {
      var track = document.getElementById("servicesTrack");
      var panels = gsap.utils.toArray(".service-panel", track);
      var counter = document.querySelector(".pin-counter .current");

      function trackDistance() {
        return track.scrollWidth - window.innerWidth + window.innerWidth * 0.06;
      }

      var horizontalTween = gsap.to(track, {
        x: function () { return -trackDistance(); },
        ease: "none",
        scrollTrigger: {
          trigger: ".services-pin",
          start: "top top",
          end: function () { return "+=" + (trackDistance() + window.innerWidth); },
          scrub: 0.6,
          pin: true,
          anticipatePin: 1,
          invalidateOnRefresh: true,
          onUpdate: function (self) {
            var idx = Math.min(panels.length, Math.max(1, Math.round(self.progress * (panels.length - 1)) + 1));
            if (counter) counter.textContent = String(idx).padStart(2, "0");
          }
        }
      });

      // Layered depth: glyphs behind each panel drift slower than the panel itself.
      panels.forEach(function (panel) {
        var glyph = panel.querySelector(".glyph");
        if (!glyph) return;
        gsap.fromTo(glyph, { x: 40 }, {
          x: -40,
          ease: "none",
          scrollTrigger: {
            trigger: panel,
            containerAnimation: horizontalTween,
            start: "left right",
            end: "right left",
            scrub: true
          }
        });
      });
    }

    /* --- Brand growth: FROM line exits, TO line arrives, gold --- */
    var fromLine = document.querySelector("[data-growth-from]");
    var toLine = document.querySelector("[data-growth-to]");
    if (fromLine && toLine) {
      gsap.set(toLine, { opacity: 0.15, y: 24 });
      gsap.timeline({
        scrollTrigger: {
          trigger: ".growth",
          start: "top top",
          end: "+=120%",
          scrub: 0.6,
          pin: true
        }
      })
        .to(fromLine, { opacity: 0.15, y: -24, scale: 0.92, ease: "none" }, 0)
        .to(toLine, { opacity: 1, y: 0, scale: 1, ease: "none" }, 0)
        .to(".growth-frame .p1", { x: 30, y: -20, rotate: 4, ease: "none" }, 0)
        .to(".growth-frame .p2", { x: -30, y: 20, rotate: -4, ease: "none" }, 0);
    }

    /* --- Showcase: horizontal gallery scroll, layered speeds --- */
    var showcaseTrack = document.getElementById("showcaseTrack");
    if (showcaseTrack && !isMobile) {
      var showcaseDistance = function () {
        return showcaseTrack.scrollWidth - window.innerWidth + window.innerWidth * 0.06;
      };
      gsap.to(showcaseTrack, {
        x: function () { return -showcaseDistance(); },
        ease: "none",
        scrollTrigger: {
          trigger: ".showcase",
          start: "top top",
          end: function () { return "+=" + showcaseDistance(); },
          scrub: 0.6,
          pin: true,
          invalidateOnRefresh: true
        }
      });
    }

    /* --- Generic reveal-on-scroll for headers, about, cta text --- */
    gsap.utils.toArray(".section-head, .about-statement, .about-foot-item, .cta h2, .eyebrow").forEach(function (el) {
      gsap.fromTo(el, { opacity: 0, y: 26 }, {
        opacity: 1, y: 0, duration: 0.9, ease: "power3.out",
        scrollTrigger: { trigger: el, start: "top 85%" }
      });
    });

    ScrollTrigger.refresh();
  }

  function initSimpleReveals() {
    // No GSAP / ScrollTrigger, or reduced motion: show everything immediately.
    document.querySelectorAll(".hero-sub, .hero-cta-row, .hero-scroll-cue, .hero-tags, .hero-tags span, .hero-kicker-logo")
      .forEach(function (el) { el.style.opacity = 1; });
    document.querySelectorAll(".hero-headline .line span")
      .forEach(function (el) { el.style.transform = "translateY(0)"; });
  }

  /* ---------------------------------------------------------
     Boot
  --------------------------------------------------------- */
  document.addEventListener("DOMContentLoaded", function () {
    initNav();
    initCursor();
    runPreloader(function () {
      initHero();
      initScrollSystem();
    });
  });

  window.addEventListener("resize", function () {
    isMobile = window.innerWidth <= 860;
    if (window.ScrollTrigger) ScrollTrigger.refresh();
  });
})();
