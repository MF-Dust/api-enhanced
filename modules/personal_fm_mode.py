from option import create_option


async def handler(query: dict, request) -> dict:
    # aidj, DEFAULT, FAMILIAR, EXPLORE, SCENE_RCMD (EXERCISE, FOCUS, NIGHT_EMO)
    data = {
        "mode": query.get("mode"),
        "subMode": query.get("submode"),
        "limit": query.get("limit", 3),
    }
    return await request("/api/v1/radio/get", data, create_option(query))
