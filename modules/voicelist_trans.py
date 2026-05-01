from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", "200"),
        "offset": query.get("offset", "0"),
        "radioId": query.get("radioId"),
        "programId": query.get("programId", "0"),
        "position": query.get("position", "1"),
    }
    return await request(
        "/api/voice/workbench/radio/program/trans", data, create_option(query)
    )
