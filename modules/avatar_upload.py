from option import create_option


async def handler(query: dict, request) -> dict:
    from plugins.upload import upload

    upload_info = await upload(query, request)
    res = await request(
        "/api/user/avatar/upload/v1",
        {"imgid": upload_info.get("imgId")},
        create_option(query),
    )
    return {
        "status": 200,
        "body": {
            "code": 200,
            "data": {
                **upload_info,
                **res.get("body", {}),
            },
        },
    }
