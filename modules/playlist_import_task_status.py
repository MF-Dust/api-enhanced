import json

from option import create_option


async def handler(query: dict, request) -> dict:
    return await request(
        "/api/playlist/import/task/status/v2",
        {
            "taskIds": json.dumps([query.get("id")]),
        },
        create_option(query),
    )
