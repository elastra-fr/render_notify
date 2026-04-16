import urllib.request
import json
from .keyring_store import get_discord_webhook


def send_discord_notification(message):
    webhook_url = get_discord_webhook()
    if not webhook_url:
        print("[RenderNotify] Discord webhook URL not found. Set it in addon preferences.")
        return

    data = {"content": message}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "RenderNotify/1.0",
    }

    try:
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
        )
        with urllib.request.urlopen(req) as response:
            if response.status == 204:
                print("[RenderNotify] Discord notification sent.")
            else:
                print(f"[RenderNotify] Discord error: HTTP {response.status}")
    except Exception as e:
        print(f"[RenderNotify] Discord error: {e}")
