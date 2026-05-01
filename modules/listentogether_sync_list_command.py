import json
from option import create_option


async def handler(query: dict, request) -> dict:
    random_list = query.get("randomList", "").split(",")
    display_list = query.get("displayList", "").split(",")
    playlist_param = json.dumps({
        "commandType": query.get("commandType"),
        "version": [
            {
                "userId": query.get("userId"),
                "version": query.get("version"),
            },
        ],
        "anchorSongId": "",
        "anchorPosition": -1,
        "randomList": random_list,
        "displayList": display_list,
    })
    data = {
        "roomId": query.get("roomId"),
        "playlistParam": playlist_param,
    }
    return await request(
        "/api/listen/together/sync/list/command/report",
        data,
        create_option(query),
    )
