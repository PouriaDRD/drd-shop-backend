import re
import requests
from django.utils import timezone
from datetime import datetime
from django.core.cache import cache


class V2raySubscriptionParser:
    timeout = 5
    cache_ttl = 60 * 2  # 1 minutes

    @classmethod
    def fetch(cls, url: str) -> dict:
        cache_key = f"vpn_sub_{url}"

        cached = cache.get(cache_key)
        if cached:
            return cached

        try:
            res = requests.get(url, timeout=cls.timeout)
            res.raise_for_status()

            data = cls.parse(res.json())

            cache.set(cache_key, data, cls.cache_ttl)
            return data

        except Exception:
            fallback = cls.fallback()
            cache.set(cache_key, fallback, 60)
            return fallback

    @classmethod
    def parse(cls, data: dict):
        remarks = data.get("remarks", "")

        remaining = cls.extract_volume(remarks)
        remaining_days = cls.extract_remaining_days(remarks)

        used = cls.calculate_used_volume(remaining)

        return {
            "remaining_volume": remaining,
            "used_volume": used,
            "status": cls.calculate_status(remaining, remaining_days, data),
        }

    @staticmethod
    def extract_volume(text: str):
        match = re.search(r"(\d+(?:\.\d+)?)\s*(KB|MB|GB|TB)📊", text)

        # ⛔️ اگر پیدا نشد => صفر
        if not match:
            return {
                "value": 0.0,
                "unit": "GB",
            }

        return {
            "value": float(match.group(1)),
            "unit": match.group(2),
        }

    @staticmethod
    def extract_remaining_days(text: str):
        match = re.search(r"(\d+)D(?:,(\d+)H)?⏳", text)
        if not match:
            return None

        days = int(match.group(1))
        hours = int(match.group(2) or 0)

        return days * 24 + hours

    @staticmethod
    def calculate_used_volume(remaining):
        if not remaining:
            return {
                "value": 0.0,
                "unit": "GB",
            }

        max_plan_gb = 100  # TODO: later from DB

        unit = remaining["unit"]
        value = remaining["value"]

        if unit == "TB":
            remaining_gb = value * 1024
        elif unit == "GB":
            remaining_gb = value
        elif unit == "MB":
            remaining_gb = value / 1024
        elif unit == "KB":
            remaining_gb = value / (1024 * 1024)
        else:
            remaining_gb = 0

        used = max(max_plan_gb - remaining_gb, 0)

        return {
            "value": round(used, 2),
            "unit": "GB",
        }

    @staticmethod
    def calculate_status(remaining, hours, data):
        expires_at = data.get("expires_at")

        if expires_at:
            try:
                exp = datetime.fromisoformat(expires_at.replace("Z", ""))
                if exp <= timezone.now().replace(tzinfo=None):
                    return "expired"
            except Exception:
                pass

        # ⛔️ fallback امن
        if not remaining or remaining["value"] <= 0:
            return "expired"

        if hours is not None and hours <= 0:
            return "expired"

        return "active"

    @staticmethod
    def fallback():
        return {
            "remaining_volume": {
                "value": 0.0,
                "unit": "GB",
            },
            "used_volume": {
                "value": 0.0,
                "unit": "GB",
            },
            "status": "unknown",
        }
