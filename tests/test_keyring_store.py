import pytest
import importlib.util
from pathlib import Path

# Load module directly to avoid importing package __init__.py (Blender deps)
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("render_notify.core.keyring_store", ROOT / "render_notify" / "core" / "keyring_store.py")
ks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ks)
import sys as _sys
_sys.modules["render_notify.core.keyring_store"] = ks


class FakeKeyring:
    class errors:
        class PasswordDeleteError(Exception):
            pass

    def __init__(self):
        self.store = {}

    def get_password(self, service, key):
        return self.store.get((service, key))

    def set_password(self, service, key, value):
        self.store[(service, key)] = value

    def delete_password(self, service, key):
        if (service, key) not in self.store:
            raise FakeKeyring.errors.PasswordDeleteError()
        del self.store[(service, key)]


def test_get_set_clear_email_credentials(monkeypatch):
    fake = FakeKeyring()
    monkeypatch.setattr(ks, "keyring", fake)

    ks.set_email_credentials("alice@example.com", "secret")
    email, password = ks.get_email_credentials()
    assert email == "alice@example.com"
    assert password == "secret"

    ks.clear_email_credentials()
    email, password = ks.get_email_credentials()
    assert email is None and password is None


def test_clear_discord_webhook_handles_missing(monkeypatch):
    fake = FakeKeyring()
    monkeypatch.setattr(ks, "keyring", fake)

    # clearing when nothing is set should not raise
    ks.clear_discord_webhook()

    ks.set_discord_webhook("https://example.com/webhook")
    assert ks.get_discord_webhook() == "https://example.com/webhook"
    ks.clear_discord_webhook()
    assert ks.get_discord_webhook() is None
