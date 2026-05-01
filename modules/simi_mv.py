from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "mvid": query.get("mvid"),
    }
    return await request("/api/discovery/simiMV", data, create_option(query, "weapi"))
