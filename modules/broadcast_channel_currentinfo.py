from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "channelId": query.get("id"),
    }
    return await request(
        "/api/voice/broadcast/channel/currentinfo", data, create_option(query)
    )
