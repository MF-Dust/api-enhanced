import json

from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "business": "Album",
        "paymentMethod": query.get("payment", ""),
        "digitalResources": json.dumps([
            {
                "business": "Album",
                "resourceID": query.get("id", ""),
                "quantity": query.get("quantity", 1),
            },
        ]),
        "from": "web",
    }
    return await request(
        "/api/ordering/web/digital",
        data,
        create_option(query, "weapi"),
    )
