from option import create_option


async def handler(query: dict, request) -> dict:
    song_id = query.get("songId")
    resource_id = query.get("resourceId")
    md5 = query.get("md5")
    filename = query.get("filename")
    song = query.get("song")
    artist = query.get("artist")
    album = query.get("album")
    bitrate = query.get("bitrate", 999000)

    if not song_id or not resource_id or not md5 or not filename:
        return {
            "status": 400,
            "body": {
                "code": 400,
                "msg": "缺少必要参数: songId, resourceId, md5, filename",
            },
        }

    import re
    song_name = song or re.sub(r"\.[^.]+$", "", filename)

    res2 = await request(
        "/api/upload/cloud/info/v2",
        {
            "md5": md5,
            "songid": song_id,
            "filename": filename,
            "song": song_name,
            "album": album or "未知专辑",
            "artist": artist or "未知艺术家",
            "bitrate": str(bitrate),
            "resourceId": resource_id,
        },
        create_option(query),
    )

    if res2.get("body", {}).get("code") != 200:
        return {
            "status": res2.get("status", 500),
            "body": {
                "code": res2.get("body", {}).get("code", 500),
                "msg": res2.get("body", {}).get("msg", "上传云盘信息失败"),
                "detail": res2.get("body"),
            },
        }

    res3 = await request(
        "/api/cloud/pub/v2",
        {"songid": res2.get("body", {}).get("songId")},
        create_option(query),
    )

    return {
        "status": 200,
        "body": {
            "code": 200,
            "data": {
                "songId": res2.get("body", {}).get("songId"),
                **res3.get("body", {}),
            },
        },
        "cookie": res2.get("cookie"),
    }
