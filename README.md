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

## Live Instagram feed

The home page strip under "Conditions we treat" loads posts from `/api/instagram`, a Vercel serverless function in `api/instagram.js`. Without a token it returns 503 and the page quietly falls back to the embedded posts listed in `INSTAGRAM_POSTS` in `tools/build-site.py`.

To enable the live feed:

1. Make sure the @care_wise_ account is a **Professional** account (Business or Creator) in the Instagram app.
2. At https://developers.facebook.com create an app, choose **Other → Business**, then add the product **Instagram → API setup with Instagram login**.
3. Under that product, add @care_wise_ as an Instagram tester and accept the invite from the account (Instagram app → Settings → Website permissions → Apps and websites → Tester invites).
4. Click **Generate token** next to the account, log in and copy the long-lived access token (valid 60 days).
5. In Vercel, Project → Settings → Environment Variables, add `INSTAGRAM_ACCESS_TOKEN` with that value, then redeploy.

`vercel.json` schedules `/api/instagram-refresh` every Monday, which extends the token's validity. If Meta ever returns a different token string, the function logs a warning and you paste the new value into Vercel. Responses are cached for an hour at the edge.

Local preview with `python -m http.server` has no `/api`, so you will always see the embed fallback locally; `vercel dev` runs the function.

## Hero background photos

Put the photos you want behind the home-page hero in `hero-images/` (JPG, PNG, HEIC or WEBP), then run `python tools/build-site.py`. They are resized into `assets/img/hero/` and the hero slides through them in filename order. One photo shows a still image; two or more slide. Delete a file and rebuild to remove it.
