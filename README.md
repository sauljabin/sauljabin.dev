# sauljabin.dev

My website. Plain HTML, CSS and JS served by GitHub Pages from the root of `main`.

```
index.html            English page (source of truth)
es/index.html         Spanish page (generated, don't edit)
assets/css/style.css  styles
assets/js/main.js     theme toggle, language preference, GitHub stars
assets/img/           pixel-art sprite and social image (generated)
favicon.svg           favicon (generated)
apple-touch-icon.png  iOS icon (generated)
tools/es.json         Spanish texts
tools/build.py         stamps asset versions, builds es/index.html
tools/pixelart.py     pixel-art source, builds the images
```

`/kaskade/`, `/kantrip/` and `/nacionalizate-ec/` are served by those repos' own
GitHub Pages, so don't create folders with those names here.

## Editing

Texts: edit `index.html`. Anything marked with `data-i18n` needs its Spanish
version in `tools/es.json`. Then rebuild the Spanish page (it fails if a
translation is missing). It also stamps `?v=<hash>` on asset URLs so
browsers never mix a new page with cached old files; run it after any change:

```bash
python3 tools/build.py
```

Pixel art: edit the grids in `tools/pixelart.py`, then regenerate the images
and the page (so the new versions are picked up):

```bash
python3 tools/pixelart.py
python3 tools/build.py
```

When the content changes, update `lastmod` in `sitemap.xml`.

## Running locally

```bash
python3 -m http.server 8123
```
