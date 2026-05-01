import re
import httpx
from option import create_option


async def handler(query: dict, request) -> dict:
    playlist_id = query.get("id", "")
    url = f"https://music.163.com/playlist?id={playlist_id}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=15.0)
        html = resp.text

    try:
        pattern = re.compile(
            r'<div class="cver u-cover u-cover-3">[\s\S]*?<img src="([^"]+)">[\s\S]*?'
            r'<a class="sname f-fs1 s-fc0" href="([^"]+)"[^>]*>([^<]+?)</a>[\s\S]*?'
            r'<a class="nm nm f-thide s-fc3" href="([^"]+)"[^>]*>([^<]+?)</a>'
        )
        playlists = []
        for match in pattern.finditer(html):
            playlists.append({
                "creator": {
                    "userId": match.group(4)[len("/user/home?id="):],
                    "nickname": match.group(5),
                },
                "coverImgUrl": match.group(1).split("?param=")[0],
                "name": match.group(3),
                "id": match.group(2)[len("/playlist?id="):],
            })
        return {
            "status": 200,
            "body": {"code": 200, "playlists": playlists},
        }
    except Exception as err:
        return {
            "status": 500,
            "body": {"code": 500, "msg": str(err)},
        }
