from option import create_option


async def handler(query: dict, request) -> dict:
    result = await request("/api/login/token/refresh", {}, create_option(query))
    if result["body"].get("code") == 200:
        return {
            "status": 200,
            "body": {
                **result["body"],
                "cookie": ";".join(result.get("cookie", [])),
            },
            "cookie": result.get("cookie", []),
        }
    return result
