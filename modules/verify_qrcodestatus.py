from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "qrCode": query.get("qr"),
    }
    res = await request(
        "/api/frontrisk/verify/qrcodestatus",
        data,
        create_option(query, "weapi"),
    )
    return res
