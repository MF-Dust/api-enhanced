import json

from option import create_option


async def handler(query: dict, request) -> dict:
    song_id = query.get("id", -2)
    artist = query.get("artist", "未知")
    album = query.get("album", "未知")

    check_data = {
        "uploadType": 0,
        "songs": json.dumps([
            {
                "md5": query.get("md5"),
                "songId": song_id,
                "bitrate": query.get("bitrate"),
                "fileSize": query.get("fileSize"),
            }
        ]),
    }
    res = await request(
        "/api/cloud/upload/check/v2", check_data, create_option(query)
    )
    # res.body.data[0].upload 0:文件可导入,1:文件已在云盘,2:不能导入
    import_data = {
        "uploadType": 0,
        "songs": json.dumps([
            {
                "songId": res.get("body", {}).get("data", [{}])[0].get("songId"),
                "bitrate": query.get("bitrate"),
                "song": query.get("song"),
                "artist": artist,
                "album": album,
                "fileName": f"{query.get('song')}.{query.get('fileType')}",
            }
        ]),
    }
    return await request(
        "/api/cloud/user/song/import", import_data, create_option(query)
    )
