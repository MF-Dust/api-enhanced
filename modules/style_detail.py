from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "tagId": query.get("tagId"),
    }
    return await request("/api/style-tag/home/head", data, create_option(query, "weapi"))
