from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "bizCode": query.get("bizCode", ""),
    }
    return await request("/api/lbs/city/code", data, create_option(query))
