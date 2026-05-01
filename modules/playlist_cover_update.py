from option import create_option


async def handler(query: dict, request) -> dict:
    if not query.get("imgFile"):
        return {
            "status": 400,
            "body": {
                "code": 400,
                "msg": "imgFile is required",
            },
        }

    from plugins.upload import image_upload
    upload_res = await image_upload(query, request)

    result = upload_res.get("body", {}).get("result", {})
    upload_info = {
        "url_pre": "https://p1.music.126.net/" + result.get("objectKey", ""),
        "imgId": result.get("docId"),
    }

    res = await request(
        "/api/playlist/cover/update",
        {
            "id": query.get("id"),
            "coverImgId": upload_info["imgId"],
        },
        create_option(query, "weapi"),
    )
    return {
        "status": 200,
        "body": {
            "code": 200,
            "data": {**upload_info, **res.get("body", {})},
        },
    }
