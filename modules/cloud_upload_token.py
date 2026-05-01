import re

import httpx

from option import create_option


async def handler(query: dict, request) -> dict:
    md5 = query.get("md5")
    file_size = query.get("fileSize")
    filename = query.get("filename")
    bitrate = query.get("bitrate", 999000)

    if not md5 or not file_size or not filename:
        return {
            "status": 400,
            "body": {
                "code": 400,
                "msg": "缺少必要参数: md5, fileSize, filename",
            },
        }

    ext = filename.rsplit(".", 1)[-1] if "." in filename else "mp3"

    check_res = await request(
        "/api/cloud/upload/check",
        {
            "bitrate": str(bitrate),
            "ext": "",
            "length": file_size,
            "md5": md5,
            "songId": "0",
            "version": 1,
        },
        create_option(query),
    )

    bucket = "jd-musicrep-privatecloud-audio-public"
    token_res = await request(
        "/api/nos/token/alloc",
        {
            "bucket": bucket,
            "ext": ext,
            "filename": re.sub(r"\.[^.]+$", "", filename)
            .replace(" ", "")
            .replace(".", "_"),
            "local": False,
            "nos_product": 3,
            "type": "audio",
            "md5": md5,
        },
        create_option(query, "weapi"),
    )

    if not token_res.get("body", {}).get("result") or not token_res["body"]["result"].get("objectKey"):
        return {
            "status": 500,
            "body": {
                "code": 500,
                "msg": "获取上传token失败",
                "detail": token_res.get("body"),
            },
        }

    try:
        async with httpx.AsyncClient() as client:
            lbs_url = f"https://wanproxy.127.net/lbs?version=1.0&bucketname={bucket}"
            resp = await client.get(lbs_url, timeout=10.0)
            lbs = resp.json()
    except Exception as error:
        return {
            "status": 500,
            "body": {
                "code": 500,
                "msg": "获取上传服务器地址失败",
                "detail": str(error),
            },
        }

    if not lbs or not lbs.get("upload") or not lbs["upload"][0]:
        return {
            "status": 500,
            "body": {
                "code": 500,
                "msg": "获取上传服务器地址无效",
                "detail": lbs,
            },
        }

    object_key = token_res["body"]["result"]["objectKey"].replace("/", "%2F")

    return {
        "status": 200,
        "body": {
            "code": 200,
            "data": {
                "needUpload": check_res.get("body", {}).get("needUpload"),
                "songId": check_res.get("body", {}).get("songId"),
                "uploadToken": token_res["body"]["result"]["token"],
                "objectKey": token_res["body"]["result"]["objectKey"],
                "resourceId": token_res["body"]["result"]["resourceId"],
                "uploadUrl": f"{lbs['upload'][0]}/{bucket}/{object_key}?offset=0&complete=true&version=1.0",
                "bucket": bucket,
                "md5": md5,
                "fileSize": file_size,
                "filename": filename,
            },
        },
        "cookie": check_res.get("cookie"),
    }
