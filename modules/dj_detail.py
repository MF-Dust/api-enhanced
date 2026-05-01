from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("rid", ""),
    }
    return await request("/api/djradio/v2/get", data, create_option(query, "weapi"))
