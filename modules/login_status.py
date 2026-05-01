from option import create_option


async def handler(query: dict, request) -> dict:
    result = await request(
        "/api/w/nuser/account/get", {}, create_option(query, "weapi")
    )
    if result["body"].get("code") == 200:
        return {
            "status": 200,
            "body": {"data": {**result["body"]}},
            "cookie": result.get("cookie", []),
        }
    return result
