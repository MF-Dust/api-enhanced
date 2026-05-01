import json

from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "cursor": json.dumps({
            "offset": 0,
            "blockCodeOrderList": ["HOMEPAGE_BLOCK_NEW_HOT_COMMENT"],
            "refresh": True,
        }),
    }
    return await request("/api/homepage/block/page", data, create_option(query))
