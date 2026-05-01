import json

from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "verifyConfigId": query.get("vid"),
        "verifyType": query.get("type"),
        "token": query.get("token"),
        "params": json.dumps({
            "event_id": query.get("evid"),
            "sign": query.get("sign"),
        }),
        "size": 150,
    }

    res = await request(
        "/api/frontrisk/verify/getqrcode",
        data,
        create_option(query, "weapi"),
    )
    qr_code = res["body"]["data"]["qrCode"]
    params_str = json.dumps({
        "event_id": query.get("evid"),
        "sign": query.get("sign"),
    })
    result_url = (
        f"https://st.music.163.com/encrypt-pages?qrCode={qr_code}"
        f"&verifyToken={query.get('token')}&verifyId={query.get('vid')}"
        f"&verifyType={query.get('type')}&params={params_str}"
    )

    try:
        import qrcode
        import io
        import base64
        qr = qrcode.make(result_url)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        qrimg = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except ImportError:
        qrimg = ""

    return {
        "status": 200,
        "body": {
            "code": 200,
            "data": {
                "qrCode": qr_code,
                "qrurl": result_url,
                "qrimg": qrimg,
            },
        },
    }
