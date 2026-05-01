from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", "200"),
        "offset": query.get("offset", "0"),
        "name": query.get("name"),
        "displayStatus": query.get("displayStatus"),
        "type": query.get("type"),
        "voiceFeeType": query.get("voiceFeeType"),
        "radioId": query.get("voiceListId"),
    }
    return await request("/api/voice/workbench/voice/list", data, create_option(query))
