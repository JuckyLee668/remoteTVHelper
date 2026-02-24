# Implementation Bootstrap (Advanced Architecture)

This repository now includes a starter implementation for the serverless remote-control architecture:

- `src/shared/protocol.py`
  - Cross-end message model and JSON serialization.
  - Includes `start_screen_stream` payload support for TV-to-phone screen viewing.
- `src/tv_app/ddns.py`
  - TV-side DDNS binding primitives.
  - Cloudflare request builder for DNS record update.
- `src/tv_app/control_service.py`
  - TV control service session and command handling skeleton.
  - Trusted-session gate and stream start behavior.
- `src/mobile_app/connection_strategy.py`
  - LAN-first / WAN-fallback connection selection.

## Next step suggestions

1. Implement actual WSS gateway in TV app (async websocket server + mTLS/pinning).
2. Implement WebRTC media pipeline for TV screen capture and mobile playback.
3. Add NAT reachability probes and UPnP mapping logic.
4. Add persistent key storage and pairing handshake protocol.


## CI/CD (GitHub Actions)

- Added `.github/workflows/android-build.yml` for building mobile and TV Android APKs.
- Build targets are expected at:
  - `apps/mobile-android`
  - `apps/tv-android`
- See `BUILD_WITH_GITHUB_ACTIONS.md` for trigger and artifact details.
