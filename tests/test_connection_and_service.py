from src.mobile_app.connection_strategy import Channel, DeviceEndpoint, choose_endpoint
from src.shared.protocol import Message, MessageType, StreamProfile
from src.tv_app.control_service import TvControlService
from src.tv_app.ddns import CloudflareDdnsClient, DdnsConfig


def test_choose_endpoint_lan_first():
    ep = DeviceEndpoint(lan_host="192.168.1.8", wan_domain="tv-home.example.net")
    channel, url = choose_endpoint(ep, lan_reachable=True)
    assert channel == Channel.LAN
    assert "192.168.1.8" in url


def test_choose_endpoint_wan_fallback():
    ep = DeviceEndpoint(lan_host=None, wan_domain="tv-home.example.net")
    channel, url = choose_endpoint(ep, lan_reachable=False)
    assert channel == Channel.WAN
    assert "tv-home.example.net" in url


def test_control_service_stream_start_requires_trust():
    svc = TvControlService()
    msg = Message(
        type=MessageType.START_SCREEN_STREAM,
        device_id="tv_001",
        payload=StreamProfile().as_payload(),
    )
    assert svc.handle_message(msg).startswith("rejected")

    svc.upsert_session("tv_001", trusted=True)
    assert svc.handle_message(msg) == "ok: screen stream started"


def test_cloudflare_ddns_request_builder():
    client = CloudflareDdnsClient(
        DdnsConfig(
            provider="cloudflare",
            zone="zone1",
            record_name="tv-home.example.net",
            token="secret",
        )
    )
    req = client.build_update_request("203.0.113.9", "record1")
    assert req["method"] == "PUT"
    assert req["json"]["content"] == "203.0.113.9"
