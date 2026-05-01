import hashlib
import os
import random
import re


class AdvancedClientSignGenerator:
    @staticmethod
    def get_real_mac_address() -> str | None:
        try:
            import netifaces
            for iface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_LINK in addrs:
                    for addr in addrs[netifaces.AF_LINK]:
                        mac = addr.get("addr", "")
                        if mac and mac != "00:00:00:00:00:00":
                            return mac.upper()
            return None
        except ImportError:
            # Fallback: try to get MAC from system
            try:
                import uuid
                mac = uuid.getnode()
                mac_str = ":".join(f"{(mac >> i) & 0xFF:02X}" for i in range(40, -1, -8))
                if mac_str != "00:00:00:00:00:00":
                    return mac_str.upper()
            except Exception:
                pass
            return None

    @staticmethod
    def generate_random_mac() -> str:
        chars = "0123456789ABCDEF"
        parts = []
        for i in range(6):
            parts.append(random.choice(chars) + random.choice(chars))
        mac = ":".join(parts)
        # Ensure unicast address (lowest bit of first byte = 0)
        first_byte = int(mac[:2], 16) & 0xFE
        return f"{first_byte:02X}" + mac[2:]

    @classmethod
    def get_mac_address(cls) -> str:
        real_mac = cls.get_real_mac_address()
        if real_mac:
            return real_mac
        return cls.generate_random_mac()

    @staticmethod
    def string_to_hex(s: str) -> str:
        return s.encode("utf-8").hex().upper()

    @staticmethod
    def sha256(data: str) -> str:
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    @classmethod
    def generate_random_device_id(cls) -> str:
        part_lengths = [4, 4, 4, 4, 4, 4, 4, 5]
        chars = "0123456789ABCDEF"
        parts = []
        for length in part_lengths:
            parts.append("".join(random.choice(chars) for _ in range(length)))
        return "_".join(parts)

    @classmethod
    def generate_random_client_sign(cls, secret_key: str = "") -> str:
        mac_address = cls.get_mac_address()
        device_id = cls.generate_random_device_id()
        hex_device_id = cls.string_to_hex(device_id)
        sign_string = f"{mac_address}@@@{hex_device_id}"
        hash_val = cls.sha256(sign_string + secret_key)
        return f"{sign_string}@@@@@@{hash_val}"

    @classmethod
    def validate_client_sign(cls, client_sign: str) -> bool:
        try:
            parts = client_sign.split("@@@@@@")
            if len(parts) != 2:
                return False
            info_part, hash_val = parts
            info_parts = info_part.split("@@@")
            if len(info_parts) != 2:
                return False
            mac, hex_device_id = info_parts
            if not re.match(r"^([0-9A-F]{2}:){5}[0-9A-F]{2}$", mac):
                return False
            if not re.match(r"^[0-9a-f]{64}$", hash_val):
                return False
            return True
        except Exception:
            return False
