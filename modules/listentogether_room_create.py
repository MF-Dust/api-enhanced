from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "refer": "songplay_more",
    }
    return await request("/api/listen/together/room/create", data, create_option(query))
