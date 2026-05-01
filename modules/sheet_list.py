from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "abTest": query.get("ab", "b"),
    }
    return await request("/api/music/sheet/list/v1", data, create_option(query))
