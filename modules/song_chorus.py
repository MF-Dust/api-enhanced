import json
from option import create_option


async def handler(query: dict, request) -> dict:
    return await request(
        "/api/song/chorus",
        {
            "ids": json.dumps([query.get("id")]),
        },
        create_option(query),
    )
