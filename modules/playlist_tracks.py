import json

from option import create_option


async def handler(query: dict, request) -> dict:
    tracks = query.get("tracks", "").split(",")
    data = {
        "op": query.get("op"),  # del, add
        "pid": query.get("pid"),  # 歌单id
        "trackIds": json.dumps(tracks),
        "imme": "true",
    }

    try:
        res = await request(
            "/api/playlist/manipulate/tracks",
            data,
            create_option(query),
        )
        return {
            "status": 200,
            "body": res,
        }
    except Exception as error:
        body = getattr(error, "body", None) or (error.args[0] if error.args else {})
        if isinstance(body, dict) and body.get("code") == 512:
            return await request(
                "/api/playlist/manipulate/tracks",
                {
                    "op": query.get("op"),
                    "pid": query.get("pid"),
                    "trackIds": json.dumps(tracks + tracks),
                    "imme": "true",
                },
                create_option(query),
            )
        else:
            return {
                "status": 200,
                "body": body,
            }
