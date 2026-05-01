import json
from datetime import datetime
from urllib.parse import quote

from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "importStarPlaylist": query.get("importStarPlaylist", False),
    }

    if query.get("local"):
        # 元数据导入
        local = json.loads(query["local"])
        multi_songs = json.dumps([
            {"songName": e["name"], "artistName": e["artist"], "albumName": e["album"]}
            for e in local
        ], ensure_ascii=False)
        data["multiSongs"] = multi_songs
    else:
        playlist_name = query.get("playlistName", f"导入音乐 {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}")
        songs = ""

        if query.get("text"):
            # 文字导入
            songs = json.dumps([{
                "name": playlist_name,
                "type": "",
                "url": f"rpc://playlist/import?text={quote(query['text'])}",
            }], ensure_ascii=False)

        if query.get("link"):
            # 链接导入
            link = json.loads(query["link"])
            songs = json.dumps([
                {"name": playlist_name, "type": "", "url": quote(e)}
                for e in link
            ], ensure_ascii=False)

        data.update({
            "playlistName": playlist_name,
            "createBusinessCode": None,
            "extParam": None,
            "taskIdForLog": "",
            "songs": songs,
        })

    return await request(
        "/api/playlist/import/name/task/create",
        data,
        create_option(query),
    )
