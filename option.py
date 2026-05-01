import os


def create_option(query: dict, crypto: str = "") -> dict:
    return {
        "crypto": query.get("crypto") or crypto or "",
        "cookie": query.get("cookie") or os.getenv("NETEASE_COOKIE", ""),
        "ua": query.get("ua", ""),
        "proxy": query.get("proxy"),
        "realIP": query.get("realIP"),
        "randomCNIP": query.get("randomCNIP", False),
        "e_r": query.get("e_r"),
        "domain": query.get("domain", ""),
        "checkToken": query.get("checkToken", False),
    }
