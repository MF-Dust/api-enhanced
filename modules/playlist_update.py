import json

from option import create_option


async def handler(query: dict, request) -> dict:
    desc = query.get("desc", "")
    tags = query.get("tags", "")
    pid = query.get("id")
    name = query.get("name", "")
    data = {
        "/api/playlist/desc/update": json.dumps({"id": pid, "desc": desc}),
        "/api/playlist/tags/update": json.dumps({"id": pid, "tags": tags}),
        "/api/playlist/update/name": json.dumps({"id": pid, "name": name}),
    }
    return await request("/api/batch", data, create_option(query))
