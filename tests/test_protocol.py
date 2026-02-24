from src.shared.protocol import Message, MessageType, StreamProfile


def test_message_roundtrip():
    msg = Message(
        type=MessageType.REMOTE_COMMAND,
        device_id="tv_001",
        payload={"command": "KEY_HOME", "repeat": 1},
        ts=123,
    )
    parsed = Message.from_json(msg.to_json())
    assert parsed == msg


def test_stream_profile_payload():
    payload = StreamProfile(max_width=640, max_fps=15).as_payload()
    assert payload["maxWidth"] == 640
    assert payload["maxFps"] == 15
