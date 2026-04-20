

bl_info = {
	"name": "Render Notify",
	"author": "Emmanuel LASTRA DE NATIAS",
	"version": (0, 1, 0),
	"blender": (4, 0, 0),
	"location": "Edit > Preferences > Add-ons",
	"description": "Send email and/or Discord notifications when a render starts, completes, or is cancelled.",
	"category": "Render",
}

# Use single source of truth for version

try:
	from ._version import __version__ as __version__
except Exception:
	__version__ = None

if __version__:
	try:
		bl_info["version"] = tuple(int(p) for p in __version__.split("."))
	except Exception:
		pass

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

def _send_async(subject, email_body, discord_message, enable_email, enable_discord, smtp_host, smtp_port, smtp_use_tls, email_cc):
	"""Run in a background thread so render is not blocked."""
	if enable_email:
		send_email_notification(subject, email_body, smtp_host, smtp_port, smtp_use_tls, email_cc)
	if enable_discord:
		send_discord_notification(discord_message)

def _notify(subject, email_body, discord_message):
	try:
		prefs = _get_prefs()
		enable_email = prefs.enable_email
		enable_discord = prefs.enable_discord
		smtp_host = prefs.smtp_host
		smtp_port = prefs.smtp_port
		smtp_use_tls = prefs.smtp_use_tls
		email_cc = prefs.email_cc
	except Exception:
		return

	if not enable_email and not enable_discord:
		return

	thread = threading.Thread(
		target=_send_async,
		args=(subject, email_body, discord_message, enable_email, enable_discord, smtp_host, smtp_port, smtp_use_tls, email_cc),
		daemon=True,
	)
	thread.start()

# ── Render handlers ────────────────────────────────────────────────────────────
@persistent
def _on_render_init(scene):
	try:
		prefs = _get_prefs()
		subject = prefs.email_subject_started
		email_body = prefs.email_body_started.replace("\\n", "\n")
		discord_message = prefs.discord_message_started.replace("\\n", "\n")
	except Exception:
		return
	_notify(subject, email_body, discord_message)

@persistent
def _on_render_complete(scene):
	try:
		prefs = _get_prefs()
		subject = prefs.email_subject_completed
		email_body = prefs.email_body_completed.replace("\\n", "\n")
		discord_message = prefs.discord_message_completed.replace("\\n", "\n")
	except Exception:
		return
	_notify(subject, email_body, discord_message)

@persistent
def _on_render_cancel(scene):
	try:
		prefs = _get_prefs()
		subject = prefs.email_subject_cancelled
		email_body = prefs.email_body_cancelled.replace("\\n", "\n")
		discord_message = prefs.discord_message_cancelled.replace("\\n", "\n")
	except Exception:
		return
	_notify(subject, email_body, discord_message)

# ── Register / Unregister ──────────────────────────────────────────────────────
def register():
	for cls in _classes:
		try:
			bpy.utils.unregister_class(cls)
		except RuntimeError:
			pass
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
