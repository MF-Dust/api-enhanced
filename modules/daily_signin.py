from option import create_option


async def handler(query: dict, request) -> dict:
    data = {"type": query.get("type", 0)}
    return await request("/api/point/dailyTask", data, create_option(query))
