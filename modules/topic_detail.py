from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "actid": query.get("actid"),
    }
    return await request("/api/act/detail", data, create_option(query, "weapi"))
