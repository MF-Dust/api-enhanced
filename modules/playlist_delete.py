from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "ids": f'[{query.get("id")}]',
    }
    return await request("/api/playlist/remove", data, create_option(query, "weapi"))
