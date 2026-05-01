from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "tag": query.get("tag"),
        "firstQuery": False,
    }
    return await request("/api/voice/sati/resource/list", data, create_option(query))
