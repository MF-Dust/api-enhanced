from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "immerseType": "c51",
        "level": query.get("level"),
    }
    return await request("/api/song/enhance/download/url/v1", data, create_option(query))
