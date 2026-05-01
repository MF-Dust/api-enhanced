import os
from dotenv import load_dotenv

load_dotenv()

# NetEase API domains
API_DOMAIN = "https://interface.music.163.com"
DOMAIN = "https://music.163.com"
ENCRYPT = True
ENCRYPT_RESPONSE = False

# Crypto constants
IV = "0102030405060708"
PRESET_KEY = "0CoJUm6Qyw8W8jud"
LINUXAPI_KEY = "rFgB&h#%2?^eDg:Q"
EAPI_KEY = "e82ckenh8dichen8"
BASE62 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

RSA_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDgtQn2JZ34ZC28NWYpAUd98iZ37BUrX/aKzmFbt7clFSs6sXqHauqKWqdtLkF2KexO40H1YTX8z2lSgBBOAxLsvaklV8k4cBFK9snQXE9/DDaFt6Rr7iVZMldczhC0JNgTz+SHXT6CBHuX3e9SdB1Ua44oncaTWz7OBGLbCiK45wIDAQAB
-----END PUBLIC KEY-----"""

# Resource type map for comments
RESOURCE_TYPE_MAP = {
    "0": "R_SO_4_",
    "1": "R_MV_5_",
    "2": "A_PL_0_",
    "3": "R_AL_3_",
    "4": "A_DJ_1_",
    "5": "R_VI_62_",
    "6": "A_EV_2_",
    "7": "A_DR_14_",
}

# Anti-cheat tokens
CLIENT_SIGN = "18:C0:4D:B9:8F:FE@@@453832335F384641365F424635335F303030315F303031425F343434415F343643365F333638332@@@@@@6ff673ef74955b38bce2fa8562d95c976ed4758b1227c4e9ee345987cee17bc9"
CHECK_TOKEN = "9ca17ae2e6ffcda170e2e6ee8af14fbabdb988f225b3868eb2c15a879b9a83d274a790ac8ff54a97b889d5d42af0feaec3b92af58cff99c470a7eafd88f75e839a9ea7c14e909da883e83fb692a3abdb6b92adee9e"

# Environment variables
CORS_ALLOW_ORIGIN = os.getenv("CORS_ALLOW_ORIGIN", "")
ENABLE_PROXY = os.getenv("ENABLE_PROXY", "false")
PROXY_URL = os.getenv("PROXY_URL", "")
ENABLE_GENERAL_UNBLOCK = os.getenv("ENABLE_GENERAL_UNBLOCK", "false")
ENABLE_FLAC = os.getenv("ENABLE_FLAC", "false")
NETEASE_COOKIE = os.getenv("NETEASE_COOKIE", "")
PORT = int(os.getenv("PORT", "3000"))
HOST = os.getenv("HOST", "")

# Global state (set by generate_config at startup)
CN_IP: str = ""
DEVICE_ID: str = ""
ANONYMOUS_TOKEN: str = ""
