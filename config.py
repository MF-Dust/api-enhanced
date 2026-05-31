from typing import Literal

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Application settings with validation."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    # NetEase API domains
    api_domain: str = Field(default="https://interface.music.163.com", description="NetEase API domain")
    domain: str = Field(default="https://music.163.com", description="NetEase main domain")
    xeapi_domain: str = Field(default="https://interface3.music.163.com", description="NetEase xeapi domain")

    # Encryption settings
    encrypt: bool = Field(default=True, description="Enable encryption")
    encrypt_response: bool = Field(default=False, description="Enable response encryption")

    # CORS settings
    cors_allow_origin: str = Field(default="", description="CORS allowed origins (comma-separated)")

    # Proxy settings
    enable_proxy: bool = Field(default=False, description="Enable proxy")
    proxy_url: str = Field(default="", description="Proxy URL")

    # Unblock settings
    enable_general_unblock: bool = Field(default=False, description="Enable general song unblock")
    enable_flac: bool = Field(default=False, description="Enable FLAC format")

    # Authentication
    netease_cookie: str = Field(default="", description="NetEase cookie for authenticated requests")

    # Server settings
    port: int = Field(default=3000, ge=1, le=65535, description="Server port")
    host: str = Field(default="", description="Server host")

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )


# Create global settings instance
settings = Settings()

# Backward compatibility: expose settings as module-level constants
API_DOMAIN = settings.api_domain
DOMAIN = settings.domain
XEAPI_DOMAIN = settings.xeapi_domain
ENCRYPT = settings.encrypt
ENCRYPT_RESPONSE = settings.encrypt_response
CORS_ALLOW_ORIGIN = settings.cors_allow_origin
ENABLE_PROXY = "true" if settings.enable_proxy else "false"
PROXY_URL = settings.proxy_url
ENABLE_GENERAL_UNBLOCK = "true" if settings.enable_general_unblock else "false"
ENABLE_FLAC = "true" if settings.enable_flac else "false"
NETEASE_COOKIE = settings.netease_cookie
PORT = settings.port
HOST = settings.host

# Crypto constants
IV = "0102030405060708"
PRESET_KEY = "0CoJUm6Qyw8W8jud"
LINUXAPI_KEY = "rFgB&h#%2?^eDg:Q"
EAPI_KEY = "e82ckenh8dichen8"
BASE62 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

RSA_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDgtQn2JZ34ZC28NWYpAUd98iZ37BUrX/aKzmFbt7clFSs6sXqHauqKWqdtLkF2KexO40H1YTX8z2lSgBBOAxLsvaklV8k4cBFK9snQXE9/DDaFt6Rr7iVZMldczhC0JNgTz+SHXT6CBHuX3e9SdB1Ua44oncaTWz7OBGLbCiK45wIDAQAB
-----END PUBLIC KEY-----"""

# xeapi constants
XEAPI_STATIC_KEY = bytes.fromhex("ab1d5a430f6bb04a3f01e81ddd72bd916d5ce591248ac128714806d7f8fb1b84")
XEAPI_SIGN_KEY = "mUHCwVNWJbunMqAHf5MImuirT6plvs6VSFW62MGHstFQxhBGdEoIhLItH3djc4+FB/OKty3+lL2rGeoFBpVe5g=="

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

# Global state (set by generate_config at startup)
CN_IP: str = ""
DEVICE_ID: str = ""
ANONYMOUS_TOKEN: str = ""
