from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "immerseType": "c51",
        "level": query.get("level"),
    }
    response = await request(
        "/api/song/enhance/download/url/v1",
        data,
        create_option(query),
    )
    url = None
    try:
        url = response.get("body", {}).get("data", [{}])[0].get("url")
    except (IndexError, KeyError, TypeError):
        pass

    if not url:
        fallback_data = {
            "ids": f"[{query.get('id')}]",
            "level": query.get("level"),
            "encodeType": "flac",
        }
        if query.get("level") == "sky":
            fallback_data["immerseType"] = "c51"
        fallback = await request(
            "/api/song/enhance/player/url/v1",
            fallback_data,
            create_option(query),
        )
        try:
            url = fallback.get("body", {}).get("data", [{}])[0].get("url")
        except (IndexError, KeyError, TypeError):
            pass

        if not url:
            return fallback

        return {
            "status": 302,
            "body": "",
            "cookie": fallback.get("cookie", []),
            "redirectUrl": url,
        }

    return {
        "status": 302,
        "body": "",
        "cookie": response.get("cookie", []),
        "redirectUrl": url,
    }
