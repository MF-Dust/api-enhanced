import json
import uuid

from option import create_option
from utils import is_one


def _create_dupkey():
    return str(uuid.uuid4())


async def handler(query: dict, request) -> dict:
    song_file = query.get("songFile")
    if not song_file:
        return {
            "status": 500,
            "body": {
                "msg": "请上传音频文件",
                "code": 500,
            },
        }

    ext = song_file.get("name", "").rsplit(".", 1)[-1] if "." in song_file.get("name", "") else ""
    filename = query.get("songName") or song_file.get("name", "").replace(f".{ext}", "").replace(" ", "").replace(".", "_")

    token_res = await request(
        "/api/nos/token/alloc",
        {
            "bucket": "ymusic",
            "ext": ext,
            "filename": filename,
            "local": False,
            "nos_product": 0,
            "type": "other",
        },
        create_option(query, "weapi"),
    )

    object_key = token_res["body"]["result"]["objectKey"].replace("/", "%2F")
    doc_id = token_res["body"]["result"]["docId"]
    nos_token = token_res["body"]["result"]["token"]

    import httpx

    # Initiate multipart upload
    async with httpx.AsyncClient() as client:
        init_res = await client.post(
            f"https://ymusic.nos-hz.163yun.com/{object_key}?uploads",
            headers={
                "x-nos-token": nos_token,
                "X-Nos-Meta-Content-Type": song_file.get("mimetype", "audio/mpeg"),
            },
        )

    import xml.etree.ElementTree as ET
    root = ET.fromstring(init_res.text)
    upload_id = root.find("UploadId").text

    file_data = song_file.get("data", b"")
    file_size = len(file_data)
    block_size = 10 * 1024 * 1024
    offset = 0
    block_index = 1
    etags = []

    async with httpx.AsyncClient() as client:
        while offset < file_size:
            chunk = file_data[offset:offset + block_size]
            part_res = await client.put(
                f"https://ymusic.nos-hz.163yun.com/{object_key}?partNumber={block_index}&uploadId={upload_id}",
                headers={
                    "x-nos-token": nos_token,
                    "Content-Type": song_file.get("mimetype", "audio/mpeg"),
                },
                content=chunk,
            )
            etag = part_res.headers.get("etag", "")
            etags.append(etag)
            offset += block_size
            block_index += 1

    # Complete multipart upload
    parts_xml = ""
    for i, etag in enumerate(etags):
        parts_xml += f"<Part><PartNumber>{i + 1}</PartNumber><ETag>{etag}</ETag></Part>"
    complete_str = f"<CompleteMultipartUpload>{parts_xml}</CompleteMultipartUpload>"

    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://ymusic.nos-hz.163yun.com/{object_key}?uploadId={upload_id}",
            headers={
                "Content-Type": "text/plain;charset=UTF-8",
                "X-Nos-Meta-Content-Type": song_file.get("mimetype", "audio/mpeg"),
                "x-nos-token": nos_token,
            },
            content=complete_str,
        )

    voice_data = json.dumps([{
        "name": filename,
        "autoPublish": is_one(query.get("autoPublish")),
        "autoPublishText": query.get("autoPublishText", ""),
        "description": query.get("description"),
        "voiceListId": query.get("voiceListId"),
        "coverImgId": query.get("coverImgId"),
        "dfsId": doc_id,
        "categoryId": query.get("categoryId"),
        "secondCategoryId": query.get("secondCategoryId"),
        "composedSongs": query.get("composedSongs", "").split(",") if query.get("composedSongs") else [],
        "privacy": is_one(query.get("privacy")),
        "publishTime": query.get("publishTime", 0),
        "orderNo": query.get("orderNo", 1),
    }])

    await request(
        "/api/voice/workbench/voice/batch/upload/preCheck",
        {
            "dupkey": _create_dupkey(),
            "voiceData": voice_data,
        },
        {
            **create_option(query),
            "headers": {"x-nos-token": nos_token},
        },
    )

    result = await request(
        "/api/voice/workbench/voice/batch/upload/v2",
        {
            "dupkey": _create_dupkey(),
            "voiceData": voice_data,
        },
        {
            **create_option(query),
            "headers": {"x-nos-token": nos_token},
        },
    )

    return {
        "status": 200,
        "body": {
            "code": 200,
            "data": result["body"]["data"],
        },
    }
