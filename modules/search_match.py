import json
from option import create_option


async def handler(query: dict, request) -> dict:
    songs = [
        {
            "title": query.get("title", ""),
            "album": query.get("album", ""),
            "artist": query.get("artist", ""),
            "duration": query.get("duration", 0),
            "persistId": query.get("md5"),
        },
    ]
    data = {
        "songs": json.dumps(songs),
    }
    return await request("/api/search/match/new", data, create_option(query))
