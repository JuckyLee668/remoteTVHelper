"""TV-side control/screen service orchestration skeleton."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from src.shared.protocol import Message, MessageType


@dataclass
class SessionContext:
    device_id: str
    trusted: bool = False
    stream_enabled: bool = False


@dataclass
class TvControlService:
    sessions: Dict[str, SessionContext] = field(default_factory=dict)

    def upsert_session(self, device_id: str, trusted: bool) -> SessionContext:
        ctx = self.sessions.get(device_id)
        if ctx is None:
            ctx = SessionContext(device_id=device_id, trusted=trusted)
            self.sessions[device_id] = ctx
        else:
            ctx.trusted = trusted
        return ctx

    def handle_message(self, message: Message) -> str:
        ctx = self.sessions.get(message.device_id)
        if ctx is None or not ctx.trusted:
            return "rejected: untrusted session"

        if message.type == MessageType.REMOTE_COMMAND:
            cmd = message.payload.get("command", "UNKNOWN")
            return f"ok: executed {cmd}"

        if message.type == MessageType.START_SCREEN_STREAM:
            ctx.stream_enabled = True
            return "ok: screen stream started"

        return "ignored"
