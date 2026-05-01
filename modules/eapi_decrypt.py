import re

from crypto import eapi_res_decrypt, eapi_req_decrypt


async def handler(query: dict, request) -> dict:
    hex_string = query.get("hexString", "")
    is_req = query.get("isReq", "true") != "false"
    if not hex_string:
        return {
            "status": 400,
            "body": {
                "code": 400,
                "message": "hex string is required",
            },
        }
    pure_hex_string = re.sub(r"\s", "", hex_string)
    return {
        "status": 200,
        "body": {
            "code": 200,
            "data": eapi_req_decrypt(pure_hex_string) if is_req else eapi_res_decrypt(pure_hex_string),
        },
    }
