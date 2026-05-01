import os
import tempfile
from pathlib import Path

from utils import generate_random_chinese_ip, generate_device_id


async def generate_config():
    """Generate startup config: random Chinese IP + anonymous token."""
    import config as cfg

    # Set global Chinese IP
    cfg.CN_IP = generate_random_chinese_ip()

    # Generate device ID
    cfg.DEVICE_ID = generate_device_id()

    # Try to get anonymous token
    try:
        from request import ncm_request
        from option import create_option

        result = await ncm_request(
            "/api/register/anonimous",
            {"username": ""},
            create_option({}, "weapi"),
        )
        cookies = result.get("cookie", [])
        for cookie in cookies:
            if "MUSIC_A=" in cookie:
                # Extract MUSIC_A value
                for part in cookie.split(";"):
                    part = part.strip()
                    if part.startswith("MUSIC_A="):
                        music_a = part.split("=", 1)[1]
                        # Save to temp file
                        tmp_path = Path(tempfile.gettempdir()) / "anonymous_token"
                        tmp_path.write_text(music_a, encoding="utf-8")
                        cfg.ANONYMOUS_TOKEN = music_a
                        break
    except Exception as e:
        print(f"Failed to register anonymous token: {e}")
        cfg.ANONYMOUS_TOKEN = ""
