import qrcode
from utils import generate_chain_id


async def handler(query: dict, request) -> dict:
    platform = query.get("platform", "pc")
    cookie = query.get("cookie", {})
    if isinstance(cookie, str):
        from utils import cookie_to_json
        cookie = cookie_to_json(cookie)

    url = f"https://music.163.com/login?codekey={query.get('key', '')}"

    if platform == "web":
        chain_id = generate_chain_id(cookie)
        url += f"&chainId={chain_id}"

    qrimg = ""
    if query.get("qrimg"):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        import io
        import base64
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        qrimg = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

    return {
        "status": 200,
        "body": {
            "code": 200,
            "data": {"qrurl": url, "qrimg": qrimg},
        },
    }
