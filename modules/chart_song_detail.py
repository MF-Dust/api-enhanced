from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "chartCode": query.get("chartCode"),
        "targetId": query.get("targetId"),
        "targetType": query.get("targetType"),
    }
    return await request("/api/chart/song/detail", data, create_option(query))
