import json
from option import create_option


async def handler(query: dict, request) -> dict:
    command_info = json.dumps({
        "commandType": query.get("commandType"),
        "progress": query.get("progress", 0),
        "playStatus": query.get("playStatus"),
        "formerSongId": query.get("formerSongId"),
        "targetSongId": query.get("targetSongId"),
        "clientSeq": query.get("clientSeq"),
    })
    data = {
        "roomId": query.get("roomId"),
        "commandInfo": command_info,
    }
    return await request(
        "/api/listen/together/play/command/report",
        data,
        create_option(query),
    )
