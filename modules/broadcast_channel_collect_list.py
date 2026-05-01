from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "contentType": "BROADCAST",
        "limit": query.get("limit", "99999"),
        "timeReverseOrder": "true",
        "startDate": "4762584922000",
    }
    return await request(
        "/api/content/channel/collect/list", data, create_option(query)
    )
