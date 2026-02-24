"""Mobile-side advanced connection strategy (LAN first, WAN fallback)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Channel(str, Enum):
    LAN = "lan"
    WAN = "wan"


@dataclass(frozen=True)
class DeviceEndpoint:
    lan_host: str | None
    wan_domain: str
    port: int = 7443


def choose_endpoint(endpoint: DeviceEndpoint, lan_reachable: bool) -> tuple[Channel, str]:
    if lan_reachable and endpoint.lan_host:
        return Channel.LAN, f"wss://{endpoint.lan_host}:{endpoint.port}"
    return Channel.WAN, f"wss://{endpoint.wan_domain}:{endpoint.port}"
