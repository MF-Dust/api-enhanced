from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "firstQuery": False,
    }
    return await request(
        "/api/voice/sati/timescene/resources/get",
        data,
        create_option(query),
    )
