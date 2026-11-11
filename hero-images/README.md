# Hero background photos

Drop the photos you want in the home-page hero here (JPG, PNG, HEIC or WEBP).
Then run from the project root:

    python tools/build-site.py

Each photo is resized to 1920px wide, saved under assets/img/hero/, and the hero
slides through them in filename order (so name them 01-..., 02-..., 03-...).
Delete a photo here and rebuild to remove it. If this folder is empty the hero
falls back to the default photo.
