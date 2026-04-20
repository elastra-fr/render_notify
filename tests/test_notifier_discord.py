import importlib.util
from pathlib import Path

# Load module directly to avoid importing Blender-dependent package __init__.py
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("render_notify.core.notifier_discord", ROOT / "render_notify" / "core" / "notifier_discord.py")
nd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nd)
import sys as _sys
_sys.modules["render_notify.core.notifier_discord"] = nd


class FakeResp:
    def __init__(self, status):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_no_webhook_prints_message(monkeypatch, capsys):
    monkeypatch.setattr(nd, "get_discord_webhook", lambda: None)
    nd.send_discord_notification("hi")
    captured = capsys.readouterr()
    assert "Discord webhook URL not found" in captured.out


def test_send_discord_success(monkeypatch, capsys):
    monkeypatch.setattr(nd, "get_discord_webhook", lambda: "https://example.com/webhook")

    def fake_urlopen(req):
        return FakeResp(204)

    monkeypatch.setattr(nd.urllib.request, "urlopen", fake_urlopen)
    nd.send_discord_notification("hello")
    captured = capsys.readouterr()
    assert "Discord notification sent" in captured.out


def test_send_discord_http_error(monkeypatch, capsys):
    monkeypatch.setattr(nd, "get_discord_webhook", lambda: "https://example.com/webhook")

    def fake_urlopen(req):
        return FakeResp(400)

    monkeypatch.setattr(nd.urllib.request, "urlopen", fake_urlopen)
    nd.send_discord_notification("hello")
    captured = capsys.readouterr()
    assert "Discord error: HTTP 400" in captured.out
