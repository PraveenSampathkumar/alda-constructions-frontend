# ALDA — Construction & Real Estate, Chennai

A single-page website for ALDA, a Chennai-based contractor and real estate developer.

The homepage hero is a **scroll-driven construction timelapse**: the scrollbar is the
playhead. Scroll down and the building assembles itself from a cleared plot to a finished
structure while a completion counter runs 0% → 100% and the copy steps through seven
phases of ALDA's story. Scroll back up and it un-builds.

## Quick start

`index.html` is completely self-contained — every image is inlined, there are no external
asset requests, and it works offline.

```
# just open it
start index.html

# or serve it
python -m http.server 8137
# → http://127.0.0.1:8137/
```

GitHub Pages works with no configuration: **Settings → Pages → Deploy from branch → `main` / `root`.**

## How the hero works

The reveal is driven by 72 stills extracted from an 8-second locked-off construction clip.

Video `currentTime` seeking was tried first and rejected — seeking forces the decoder to
jump to a keyframe and decode forward on every scroll tick, which stutters badly and no
amount of JavaScript smooths it. Instead the frames are decoded **once** into
`ImageBitmap`s at load, and scrolling only calls `drawImage` on a canvas. The scrub cost is
then a single blit regardless of scroll speed.

Scroll position maps to a frame index, a completion percentage interpolated between phase
values, a phase label, and a progress bar. Below the hero, an `IntersectionObserver` drives
staggered section reveals and the counting figures — each fires once, then unobserves.

## Structure

```
index.html                    built, self-contained site (open this)
src/
  head.html                   design tokens, typography, component CSS
  hero.html                   sticky timelapse hero markup + styles
  extra.html                  build process, figures, capabilities, crane, CTA
  home.html                   hero + extra, spliced (generated)
  pages.html                  About, What We Do, Projects, Locations, NRI,
                              Insights, Careers, Contact, Legal
  nav-footer.html             nav and footer source
  script.html                 scrubber, reveals, counters, router, form
assets/
  frames/                     72 stills, the timelapse source
  photo.jpg                   site photograph
  sky_plate.jpg               sky extracted from the photo (earlier CSS reveal)
  construction-reveal.mp4     original 8s clip
tools/
  extract_frames.py           MP4 → 72 stills (Blender, headless)
  make_sky_plate.py           builds the sky plate from the photograph
  build.py                    inlines everything into index.html
```

## Rebuilding

Frame extraction needs Blender (headless, no GUI):

```
blender -b --factory-startup --python tools/extract_frames.py   # → assets/frames/
python tools/build.py                                            # → index.html
```

Paths inside the tool scripts are absolute and point at the original working directory —
adjust them before running elsewhere.

## Design

Fraunces for display (a heritage serif, for a business tracing to 1913), Karla for body,
IBM Plex Mono for figures and labels. Warm architectural off-white with dark immersive
bands and a grounded amber accent. Light and dark themes are both defined at token level.
`prefers-reduced-motion` is respected throughout.

## Content status

Copy, contact details and project data are ALDA's own. Four areas are **deliberately left
empty** pending client confirmation, and should not be filled with placeholder content:

- **Team** — Vijay Srinivas is named and described, but no designation is shown
- **Awards & Recognition** — no claims until verified awards are supplied
- **Testimonials** — verified, client-approved testimonials only
- **ALDA Aran** — location, configuration, units and RERA all read "to be confirmed"

## Known limitations

- The enquiry form opens a pre-filled email to `info@aldaglobal.com`. There is no backend;
  wiring it to a CRM or form handler is a hosting-side task.
- `index.html` is ~8.9 MB because every frame is inlined. Splitting the frames back out as
  separate files would cut initial payload at the cost of self-containment.
- Hero imagery is an architectural visualisation and is labelled as such in the footer.
