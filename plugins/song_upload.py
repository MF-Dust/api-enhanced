import hashlib
import httpx
from option import create_option


async def song_upload(query: dict, request) -> dict:
    """Cloud song upload via NOS."""
    song_file = query.get("songFile", {})
    ext = song_file.get("name", "").rsplit(".", 1)[-1] if "." in song_file.get("name", "") else "mp3"
    filename = song_file.get("name", "unknown.mp3")
    bucket = "jd-musicrep-privatecloud-audio-public"

    # Allocate upload token
    token_res = await request(
        "/api/nos/token/alloc",
        {
            "bucket": bucket,
            "ext": ext,
            "filename": filename,
            "local": False,
            "nos_product": 3,
            "type": "audio",
            "md5": song_file.get("md5", ""),
        },
        create_option(query, "weapi"),
    )

    if not token_res.get("body", {}).get("result", {}).get("objectKey"):
        return {
            "status": 500,
            "body": {"code": 500, "msg": "获取上传token失败", "detail": token_res.get("body")},
        }

    object_key = token_res["body"]["result"]["objectKey"].replace("/", "%2F")

    # Get LBS endpoint
    try:
        async with httpx.AsyncClient() as client:
            lbs_resp = await client.get(
                f"https://wanproxy.127.net/lbs?version=1.0&bucketname={bucket}",
                timeout=10.0,
            )
            lbs = lbs_resp.json()
    except Exception as e:
        return {
            "status": 500,
            "body": {"code": 500, "msg": "获取上传服务器地址失败", "detail": str(e)},
        }

    if not lbs.get("upload") or not lbs["upload"][0]:
        return {
            "status": 500,
            "body": {"code": 500, "msg": "获取上传服务器地址无效", "detail": lbs},
        }

    # Upload file
    upload_url = f"{lbs['upload'][0]}/{bucket}/{object_key}?offset=0&complete=true&version=1.0"
    file_data = song_file.get("data", b"")
    if hasattr(file_data, "read"):
        file_data = file_data.read()

    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                upload_url,
                content=file_data,
                headers={
                    "x-nos-token": token_res["body"]["result"]["token"],
                    "Content-MD5": song_file.get("md5", ""),
                    "Content-Type": song_file.get("mimetype", "audio/mpeg"),
                    "Content-Length": str(len(file_data)),
                },
                timeout=300.0,
            )
    except Exception as e:
        return {
            "status": 500,
            "body": {"code": 500, "msg": "文件上传失败", "detail": str(e)},
        }

    return token_res
