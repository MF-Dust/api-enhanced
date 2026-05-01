from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "programId": query.get("id"),
    }
    return await request("/api/voice/lyric/get", data, create_option(query))
