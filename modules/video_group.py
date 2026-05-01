from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "groupId": query.get("id"),
        "offset": query.get("offset", 0),
        "need_preview_url": "true",
        "total": True,
    }
    return await request(
        "/api/videotimeline/videogroup/otherclient/get",
        data,
        create_option(query, "weapi"),
    )
