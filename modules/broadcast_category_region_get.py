from option import create_option


async def handler(query: dict, request) -> dict:
    return await request(
        "/api/voice/broadcast/category/region/get", {}, create_option(query)
    )
