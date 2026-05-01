from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "offset": query.get("offset", 0),
        "filterLives": "[]",
        "withProgramInfo": "true",
        "needUrl": "1",
        "resolution": "480",
    }
    return await request("/api/videotimeline/get", data, create_option(query, "weapi"))
