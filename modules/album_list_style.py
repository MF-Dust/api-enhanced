from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 10),
        "offset": query.get("offset", 0),
        "total": True,
        "area": query.get("area", "Z_H"),  # Z_H:华语,E_A:欧美,KR:韩国,JP:日本
    }
    return await request(
        "/api/vipmall/appalbum/album/style", data, create_option(query, "weapi")
    )
