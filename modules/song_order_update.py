from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "pid": query.get("pid"),
        "trackIds": query.get("ids"),
        "op": "update",
    }
    return await request("/api/playlist/manipulate/tracks", data, create_option(query))
