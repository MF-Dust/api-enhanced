import json

from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "artistId": query.get("id"),
        "page": json.dumps({
            "size": query.get("size", 10),
            "cursor": query.get("cursor", 0),
        }),
        "tab": 0,
        "order": query.get("order", 0),
    }
    return await request(
        "/api/mlog/artist/video", data, create_option(query, "weapi")
    )
