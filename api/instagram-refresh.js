// Vercel cron target: refreshes the long-lived Instagram token so it does not
// expire after 60 days. Meta usually returns the same token with a new expiry;
// if the returned token differs, this logs a warning so you can update the
// INSTAGRAM_ACCESS_TOKEN environment variable in Vercel.

module.exports = async function handler(req, res) {
  const token = process.env.INSTAGRAM_ACCESS_TOKEN;
  if (!token) {
    res.status(503).json({ error: "INSTAGRAM_ACCESS_TOKEN is not configured" });
    return;
  }
  // Only Vercel Cron (or someone holding CRON_SECRET) may trigger this.
  const auth = req.headers.authorization || "";
  if (process.env.CRON_SECRET && auth !== "Bearer " + process.env.CRON_SECRET) {
    res.status(401).json({ error: "Unauthorized" });
    return;
  }
  try {
    const r = await fetch(
      "https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=" +
        encodeURIComponent(token)
    );
    const data = await r.json();
    if (!r.ok || data.error) {
      res.status(502).json({ error: (data.error && data.error.message) || "Refresh failed" });
      return;
    }
    const changed = data.access_token && data.access_token !== token;
    if (changed) console.warn("Instagram returned a new token; update INSTAGRAM_ACCESS_TOKEN in Vercel.");
    res.status(200).json({ ok: true, expires_in_days: Math.round((data.expires_in || 0) / 86400), token_changed: !!changed });
  } catch (e) {
    res.status(502).json({ error: "Could not reach Instagram" });
  }
};
