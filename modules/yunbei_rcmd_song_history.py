import json

from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "page": json.dumps({
            "size": query.get("size", 20),
            "cursor": query.get("cursor", ""),
        }),
    }
    return await request(
        "/api/yunbei/rcmd/song/history/list", data, create_option(query, "weapi")
    )
