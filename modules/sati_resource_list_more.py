from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
    }
    return await request(
        "/api/voice/sati/resource/list/more/v1",
        data,
        create_option(query),
    )
