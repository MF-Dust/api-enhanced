import json
from option import create_option


async def handler(query: dict, request) -> dict:
    ids = query.get("ids", "")
    if isinstance(ids, str):
        ids = [id.strip() for id in ids.split(",") if id.strip()]
    tracks = json.dumps([{"type": 3, "id": id} for id in ids])
    data = {"id": query.get("id", ""), "tracks": tracks}
    return await request("/api/playlist/track/delete", data, create_option(query, "weapi"))
