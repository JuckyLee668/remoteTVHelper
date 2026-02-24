"""Shared protocol models for mobile <-> TV communication."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from typing import Any, Dict


class MessageType(str, Enum):
    REMOTE_COMMAND = "remote_command"
    TV_STATE = "tv_state"
    DDNS_STATUS = "ddns_status"
    START_SCREEN_STREAM = "start_screen_stream"


@dataclass(frozen=True)
class Message:
    type: MessageType
    device_id: str
    payload: Dict[str, Any]
    ts: int | None = None

    def to_json(self) -> str:
        body = {
            "type": self.type.value,
            "deviceId": self.device_id,
            "payload": self.payload,
        }
        if self.ts is not None:
            body["ts"] = self.ts
        return json.dumps(body, ensure_ascii=False, separators=(",", ":"))

    @staticmethod
    def from_json(raw: str) -> "Message":
        data = json.loads(raw)
        msg_type = MessageType(data["type"])
        return Message(
            type=msg_type,
            device_id=data["deviceId"],
            payload=data.get("payload", {}),
            ts=data.get("ts"),
        )


@dataclass(frozen=True)
class StreamProfile:
    video_codec: str = "h264"
    max_width: int = 1280
    max_fps: int = 20
    profile: str = "low_latency"

    def as_payload(self) -> Dict[str, Any]:
        return {
            "videoCodec": self.video_codec,
            "maxWidth": self.max_width,
            "maxFps": self.max_fps,
            "profile": self.profile,
        }
