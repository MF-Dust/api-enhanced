from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", "200"),
        "offset": query.get("offset", "0"),
        "voiceListId": query.get("voiceListId"),
    }
    return await request(
        "/api/voice/workbench/voices/by/voicelist", data, create_option(query)
    )
