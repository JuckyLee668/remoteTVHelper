"""TV-side DDNS binding primitives."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class DdnsConfig:
    provider: str
    zone: str
    record_name: str
    token: str
    ttl: int = 60


class CloudflareDdnsClient:
    api_base = "https://api.cloudflare.com/client/v4"

    def __init__(self, config: DdnsConfig) -> None:
        if config.provider.lower() != "cloudflare":
            raise ValueError("CloudflareDdnsClient only supports provider=cloudflare")
        self.config = config

    def build_update_request(self, ip: str, record_id: str) -> Dict[str, object]:
        return {
            "method": "PUT",
            "url": f"{self.api_base}/zones/{self.config.zone}/dns_records/{record_id}",
            "headers": {
                "Authorization": f"Bearer {self.config.token}",
                "Content-Type": "application/json",
            },
            "json": {
                "type": "A",
                "name": self.config.record_name,
                "content": ip,
                "ttl": self.config.ttl,
                "proxied": False,
            },
        }
