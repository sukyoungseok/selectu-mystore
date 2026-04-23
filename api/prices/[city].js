export default async function handler(req, res) {
    const { city } = req.query;
    const directOnly = req.query.directOnly ?? "false";

    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Cache-Control", "s-maxage=3600, stale-while-revalidate=7200");

    try {
        const upstream = await fetch(
            `https://tripsignal.vercel.app/api/prices/${city}?directOnly=${directOnly}`,
        );
        if (!upstream.ok) {
            return res.status(upstream.status).json({ error: "upstream error" });
        }
        const data = await upstream.json();
        return res.status(200).json(data);
    } catch (e) {
        return res.status(502).json({ error: "fetch failed", detail: e.message });
    }
}
