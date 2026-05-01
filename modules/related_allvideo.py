import re
from option import create_option


async def handler(query: dict, request) -> dict:
    song_id = query.get("id", "")
    data = {
        "id": song_id,
        "type": 0 if re.match(r"^\d+$", song_id) else 1,
    }
    return await request(
        "/api/cloudvideo/v1/allvideo/rcmd",
        data,
        create_option(query, "weapi"),
    )
