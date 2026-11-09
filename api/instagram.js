// Vercel serverless function: returns the latest @care_wise_ posts as JSON.
// Needs INSTAGRAM_ACCESS_TOKEN (long-lived token from "Instagram API with
// Instagram Login") in the project's environment variables. Responses are
// cached at the edge for an hour, so Instagram is called at most ~24x/day.

const FIELDS = "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp";

module.exports = async function handler(req, res) {
  const token = process.env.INSTAGRAM_ACCESS_TOKEN;
  res.setHeader("Access-Control-Allow-Origin", "*");

  if (!token) {
    res.status(503).json({ error: "INSTAGRAM_ACCESS_TOKEN is not configured" });
    return;
  }

  const limit = Math.min(parseInt(req.query.limit, 10) || 12, 24);
  const url =
    "https://graph.instagram.com/me/media?fields=" + FIELDS +
    "&limit=" + limit + "&access_token=" + encodeURIComponent(token);

  try {
    const r = await fetch(url);
    const data = await r.json();
    if (!r.ok || data.error) {
      res.setHeader("Cache-Control", "s-maxage=300");
      res.status(502).json({ error: (data.error && data.error.message) || "Instagram request failed" });
      return;
    }
    const items = (data.data || [])
      .filter((m) => m.media_type !== "CAROUSEL_ALBUM" || m.media_url)
      .map((m) => ({
        id: m.id,
        type: m.media_type,
        image: m.media_type === "VIDEO" ? m.thumbnail_url || m.media_url : m.media_url,
        caption: (m.caption || "").slice(0, 160),
        url: m.permalink,
        time: m.timestamp,
      }));
    res.setHeader("Cache-Control", "s-maxage=3600, stale-while-revalidate=86400");
    res.status(200).json({ items });
  } catch (e) {
    res.setHeader("Cache-Control", "s-maxage=300");
    res.status(502).json({ error: "Could not reach Instagram" });
  }
};
