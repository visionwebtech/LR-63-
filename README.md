# LR-63 — Digital Marketing & Brand Growth (website)

Plain HTML/CSS/JS. No build step, no npm install. Animation is powered by
[GSAP](https://gsap.com) + ScrollTrigger, loaded from a CDN.

## Run it locally

Just double-clicking `index.html` will mostly work, but the preloader reads
pixel data off the logo with `canvas.getImageData`, which some browsers
block on `file://` pages. Serve it over a tiny local server instead:

```bash
cd lr63-site
python3 -m http.server 8080
# then open http://localhost:8080
```

or, if you have Node:

```bash
npx serve .
```

## Deploy it (GitHub Pages)

1. Push this folder's contents to a repo (keep `index.html` at the repo
   root, or in the folder you point Pages at).
2. Repo → Settings → Pages → Deploy from branch → `main` / `/root`.
3. Done — no build step needed.

## What's in here

```
index.html          all sections, in scroll order
css/style.css        design tokens at the top (:root), then per-section styles
js/main.js            preloader particle-logo build, custom cursor, nav,
                       hero reveal, GSAP ScrollTrigger scroll system
assets/img/lr63-logo.png   your uploaded logo, used as-is (not redrawn)
```

## How the motion system works

- **Preloader** — samples the logo PNG's bright pixels into a point cloud,
  scatters them randomly, then animates them to their real position
  (`js/main.js`, `runPreloader`). This is why it needs a local server, not
  `file://`.
- **Services section** — pinned with `ScrollTrigger`; vertical scroll
  drives a horizontal `x` transform on the panel track (the
  "vertical scroll → horizontal movement" behavior from the brief).
  On screens ≤860px this pin is disabled and replaced with a normal
  swipeable row (`.services-swipe`), since scroll-jacking fights with
  touch scrolling.
- **Brand growth section** — also pinned; one line fades/scales out while
  the gold line fades/scales in, scrubbed to scroll position.
- **Showcase** — same horizontal-scroll-via-vertical-scroll pattern as
  Services, at a different pace, for the layered-depth feel.
- **Reduced motion** — `prefers-reduced-motion` is checked up front. If
  set, the preloader just fades out and everything else appears in place
  with no pinning or scrubbing.

## What I couldn't do exactly as asked

The brief asked for AI-generated premium campaign photography throughout.
I don't have an image-generation tool in this environment, so the
showcase panels and service-panel backgrounds are gold/black gradient
"mesh" placeholders (`.art-mesh-1` … `.art-mesh-5` in `style.css`) rather
than real photos — same layout and motion, temporary art. Swap them for
real photography or AI renders whenever you have them; each one is a
single `<div class="art ...">` you can turn into `<img>` or a
`background-image`.

## What I'd extend first

1. **Real imagery** — replace the `.art-mesh-*` gradient panels with
   actual campaign photos/renders. Layout and animation don't change.
2. **Contact form** — the CTA button is currently a `mailto:` link.
   Swap in a real form (Formspree, a serverless function, whatever you're
   already using) once you have a backend to send it to.
3. **Lenis smooth-scroll** — GSAP's ScrollTrigger works fine with native
   scroll, but if you want the buttery inertia scroll from the reference
   video specifically, add [Lenis](https://lenis.darkroom.engineering/)
   and hook its `scroll` event into `ScrollTrigger.update` — a few lines
   in `main.js`.
4. **Case study pages** — each showcase card is a good candidate to link
   out to a real project page once you have real client work to show.
5. **Analytics/SEO** — add real Open Graph tags, a favicon set, and
   whatever analytics snippet you use once the domain is live.
