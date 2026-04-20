import types
import importlib.util
from pathlib import Path

# Load module directly to avoid importing Blender-dependent package __init__.py
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("render_notify.core.notifier_email", ROOT / "render_notify" / "core" / "notifier_email.py")
ne = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ne)
import sys as _sys
_sys.modules["render_notify.core.notifier_email"] = ne


def test_no_credentials_prints_message(monkeypatch, capsys):
    monkeypatch.setattr(ne, "get_email_credentials", lambda: (None, None))
    ne.send_email_notification("subject", "message")
    captured = capsys.readouterr()
    assert "Email credentials not found" in captured.out


def test_send_email_success_ssl(monkeypatch, capsys):
    monkeypatch.setattr(ne, "get_email_credentials", lambda: ("me@example.com", "pw"))

    class FakeServer:
        def login(self, email, pw):
            assert email == "me@example.com"
            assert pw == "pw"

        def sendmail(self, from_addr, recipients, msg):
            assert from_addr == "me@example.com"
            assert "Subject" in msg

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(ne, "smtplib", types.SimpleNamespace(SMTP_SSL=lambda host, port: FakeServer(), SMTP=lambda host, port: FakeServer()))
    ne.send_email_notification("subject", "message", use_tls=False)
    captured = capsys.readouterr()
    assert "Email sent successfully" in captured.out


def test_send_email_success_tls(monkeypatch, capsys):
    monkeypatch.setattr(ne, "get_email_credentials", lambda: ("me@example.com", "pw"))

    class FakeSMTP:
        def starttls(self):
            pass

        def login(self, email, pw):
            assert email == "me@example.com"
            assert pw == "pw"

        def sendmail(self, from_addr, recipients, msg):
            assert from_addr == "me@example.com"

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(ne, "smtplib", types.SimpleNamespace(SMTP=lambda host, port: FakeSMTP(), SMTP_SSL=lambda host, port: FakeSMTP()))
    ne.send_email_notification("subject", "message", use_tls=True)
    captured = capsys.readouterr()
    assert "Email sent successfully" in captured.out
