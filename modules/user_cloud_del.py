from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "songIds": [query.get("id")],
    }
    return await request("/api/cloud/del", data, create_option(query, "weapi"))
