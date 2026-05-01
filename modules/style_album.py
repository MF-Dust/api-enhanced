from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "cursor": query.get("cursor", 0),
        "size": query.get("size", 20),
        "tagId": query.get("tagId"),
        "sort": query.get("sort", 0),
    }
    return await request(
        "/api/style-tag/home/album", data, create_option(query, "weapi")
    )
