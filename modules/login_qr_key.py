from option import create_option


async def handler(query: dict, request) -> dict:
    data = {"type": 3}
    result = await request("/api/login/qrcode/unikey", data, create_option(query))
    return {
        "status": 200,
        "body": {"data": result["body"], "code": 200},
        "cookie": result.get("cookie", []),
    }
