import json

from option import create_option


async def handler(query: dict, request) -> dict:
    return await request(
        "/api/social/user/status/edit",
        {
            "content": json.dumps({
                "type": query.get("type"),
                "iconUrl": query.get("iconUrl"),
                "content": query.get("content"),
                "actionUrl": query.get("actionUrl"),
            }),
        },
        create_option(query),
    )
