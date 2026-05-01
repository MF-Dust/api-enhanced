from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "moduleId": query.get("moduleId", "1207signin-1207signin"),
    }
    return await request(
        "/api/act/modules/signin/v2/progress",
        data,
        create_option(query, "weapi"),
    )
