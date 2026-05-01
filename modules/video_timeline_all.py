from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "groupId": 0,
        "offset": query.get("offset", 0),
        "need_preview_url": "true",
        "total": True,
    }
    return await request(
        "/api/videotimeline/otherclient/get",
        data,
        create_option(query, "weapi"),
    )
