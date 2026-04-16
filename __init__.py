bl_info = {
    "name": "Render Notify",
    "author": "Emmanuel LASTRA DE NATIAS",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "location": "Edit > Preferences > Add-ons",
    "description": "Send email and/or Discord notifications when a render starts, completes, or is cancelled.",
    "category": "Render",
}

import threading

import bpy
from bpy.app.handlers import persistent

from .core.notifier_email import send_email_notification
from .core.notifier_discord import send_discord_notification
from .ui.preferences import (
    RenderNotifyPreferences,
    SetEmailCredentialsOperator,
    ClearEmailCredentialsOperator,
    SetDiscordWebhookOperator,
    ClearDiscordWebhookOperator,
)

ADDON_ID = __name__  # "render_notify"

_classes = [
    RenderNotifyPreferences,
    SetEmailCredentialsOperator,
    ClearEmailCredentialsOperator,
    SetDiscordWebhookOperator,
    ClearDiscordWebhookOperator,
]


# ── Notification helpers ───────────────────────────────────────────────────────

def _get_prefs():
    return bpy.context.preferences.addons[ADDON_ID].preferences


def _send_async(subject, message, enable_email, enable_discord, smtp_host, smtp_port):
    """Run in a background thread so render is not blocked."""
    if enable_email:
        send_email_notification(subject, message, smtp_host, smtp_port)
    if enable_discord:
        send_discord_notification(message)


def _notify(subject, message):
    try:
        prefs = _get_prefs()
        enable_email = prefs.enable_email
        enable_discord = prefs.enable_discord
        smtp_host = prefs.smtp_host
        smtp_port = prefs.smtp_port
    except Exception:
        return

    if not enable_email and not enable_discord:
        return

    thread = threading.Thread(
        target=_send_async,
        args=(subject, message, enable_email, enable_discord, smtp_host, smtp_port),
        daemon=True,
    )
    thread.start()


# ── Render handlers ────────────────────────────────────────────────────────────

@persistent
def _on_render_init(scene):
    filepath = bpy.data.filepath or "Untitled"
    _notify(
        "Render Started",
        f"\U0001f3a8 Render **started**\nFile: {filepath}",
    )


@persistent
def _on_render_complete(scene):
    filepath = bpy.data.filepath or "Untitled"
    _notify(
        "Render Complete",
        f"\u2705 Render **completed**\nFile: {filepath}",
    )


@persistent
def _on_render_cancel(scene):
    filepath = bpy.data.filepath or "Untitled"
    _notify(
        "Render Cancelled",
        f"\u274c Render **cancelled / failed**\nFile: {filepath}",
    )


# ── Register / Unregister ──────────────────────────────────────────────────────

def register():
    for cls in _classes:
        bpy.utils.register_class(cls)
    bpy.app.handlers.render_init.append(_on_render_init)
    bpy.app.handlers.render_complete.append(_on_render_complete)
    bpy.app.handlers.render_cancel.append(_on_render_cancel)


def unregister():
    for handler, lst in (
        (_on_render_init, bpy.app.handlers.render_init),
        (_on_render_complete, bpy.app.handlers.render_complete),
        (_on_render_cancel, bpy.app.handlers.render_cancel),
    ):
        if handler in lst:
            lst.remove(handler)
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
