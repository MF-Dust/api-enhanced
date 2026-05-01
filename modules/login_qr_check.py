from option import create_option


async def handler(query: dict, request) -> dict:
    data = {"key": query.get("key", ""), "type": 3}
    try:
        result = await request(
            "/api/login/qrcode/client/login", data, create_option(query)
        )
        return {
            "status": 200,
            "body": {
                **result["body"],
                "cookie": ";".join(result.get("cookie", [])),
            },
            "cookie": result.get("cookie", []),
        }
    except Exception:
        return {"status": 200, "body": {}, "cookie": []}
