from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "cancel": query.get("cancel", False),
    }
    return await request("/api/voice/sati/resource/sub", data, create_option(query))
