# Carewise website

Static marketing site for Carewise Healthcare, Mysuru. No build step is needed to deploy: every page is a plain HTML file at the repository root with assets under `assets/`.

## Editing content

All page copy lives in `tools/build-site.py`. After editing, regenerate the HTML:

```bash
python tools/build-site.py
```

Styles are in `assets/css/site.css` (layout and theme) and `assets/css/motion.css` (animations). Behaviour is in `assets/js/site.js` and `assets/js/motion.js`.

## Local preview

```bash
python -m http.server 8080
```

Then open http://localhost:8080/.

## Deploying on Vercel

Import the repository in Vercel with framework preset **Other** and no build command. `vercel.json` enables clean URLs, so `/about.html` is served at `/about`, and sets long cache headers for `assets/`.
