import bpy
from bpy.props import BoolProperty, IntProperty, StringProperty
from ..core.keyring_store import (
	get_email_credentials,
	set_email_credentials,
	clear_email_credentials,
	get_discord_webhook,
	set_discord_webhook,
	clear_discord_webhook,
)

# Resolve the root package name (render_notify) from render_notify.ui
_ADDON_ID = __package__.rsplit(".", 1)[0]


class RenderNotifyPreferences(bpy.types.AddonPreferences):

	# Préférences for notifications messages 

		## Email notifications messages

	email_subject_started: StringProperty(
		name="Email Subject - Render Started",
		default="Render Started",
	)
	email_body_started: StringProperty(
		name="Email Body - Render Started",
		description="Use \\n+ for line breaks",
		default="Your render has started. We will notify you when it's completed or if it gets cancelled.",
	)
	email_subject_completed: StringProperty(
		name="Email Subject - Render Completed",
		default="Render Completed",
	)
	email_body_completed: StringProperty(
		name="Email Body - Render Completed",
		description="Use \\n+ for line breaks",
		default="Your render has completed successfully.",
	)
	email_subject_cancelled: StringProperty(
		name="Email Subject - Render Cancelled",
		default="Render Cancelled",
	)
	email_body_cancelled: StringProperty(
		name="Email Body - Render Cancelled",
		description="Use \\n+ for line breaks",
		default="Your render was cancelled.",
	)

		# Discord notifications messages

	discord_message_started: StringProperty(
		name="Discord Message - Render Started",
		description="Use \\n+ for line breaks",
		default=":clapper: Render Started! We will notify you when it's completed or if it gets cancelled.",
	)
	discord_message_completed: StringProperty(
		name="Discord Message - Render Completed",
		description="Use \\n+ for line breaks",
		default=":tada: Render Completed! Your render has completed successfully.",
	)
	discord_message_cancelled: StringProperty(
		name="Discord Message - Render Cancelled",
		description="Use \\n+ for line breaks",
		default=":x: Render Cancelled! Your render was cancelled.",
	)

	bl_idname = _ADDON_ID

	enable_email: BoolProperty(
		name="Enable Email Notifications",
		default=False,
	)
	smtp_host: StringProperty(
		name="SMTP Host",
		default="smtp.gmail.com",
	)
	smtp_port: IntProperty(
		name="SMTP Port",
		default=465,
		min=1,
		max=65535,
	)
	smtp_use_tls: BoolProperty(
		name="Use STARTTLS",
		description="Use STARTTLS (port 587) instead of SSL (port 465). Required for Outlook, Yahoo, OVH, etc.",
		default=False,
	)
	email_cc: StringProperty(
		name="CC",
		description="Additional recipients, comma-separated (e.g. alice@example.com, bob@example.com)",
		default="",
	)
	enable_discord: BoolProperty(
		name="Enable Discord Notifications",
		default=False,
	)

	def draw(self, context):
		layout = self.layout

		# Email section
		box = layout.box()
		box.prop(self, "enable_email")
		if self.enable_email:
			email, pw = get_email_credentials(), None
			try:
				email, pw = get_email_credentials()
			except Exception:
				email = None

			if email and pw:
				box.label(text=f"Sender: {email}", icon="CHECKMARK")
				box.operator(
					"render_notify.clear_email_credentials",
					text="Clear Email Credentials",
					icon="X",
				)

				box.label(text="Notification Messages:", icon="INFO")
				box.prop(self, "email_subject_started")
				box.prop(self, "email_body_started")
				box.prop(self, "email_subject_completed")
				box.prop(self, "email_body_completed")
				box.prop(self, "email_subject_cancelled")
				box.prop(self, "email_body_cancelled")
			else:
				box.label(text="No credentials set.", icon="ERROR")
				box.operator(
					"render_notify.set_email_credentials",
					text="Set Email Credentials",
					icon="PLUS",
				)

		# Discord section
		box = layout.box()
		box.prop(self, "enable_discord")
		if self.enable_discord:
			webhook = get_discord_webhook()
			if webhook:
				box.label(text="Webhook URL: configured", icon="CHECKMARK")
				box.operator(
					"render_notify.clear_discord_webhook",
					text="Clear Discord Webhook",
					icon="X",
				)

				box.label(text="Notification Messages:", icon="INFO")
				box.prop(self, "discord_message_started")
				box.prop(self, "discord_message_completed")
				box.prop(self, "discord_message_cancelled")
			else:
				box.label(text="No webhook set.", icon="ERROR")
				box.operator(
					"render_notify.set_discord_webhook",
					text="Set Discord Webhook",
					icon="PLUS",
				)


# ── Operators ──────────────────────────────────────────────────────────────────

class SetEmailCredentialsOperator(bpy.types.Operator):
	bl_idname = "render_notify.set_email_credentials"
	bl_label = "Set Email Credentials"
	bl_description = "Save email and password to system keyring"

	email: StringProperty(name="Email")
	password: StringProperty(name="Password", subtype="PASSWORD")

	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self, width=520)

	def draw(self, context):
		layout = self.layout
		layout.prop(self, "email")
		layout.prop(self, "password")

	def execute(self, context):
		if not self.email or not self.password:
			self.report({"ERROR"}, "Email and password required.")
			return {"CANCELLED"}
		set_email_credentials(self.email, self.password)
		self.report({"INFO"}, "Email credentials saved.")
		return {"FINISHED"}


class ClearEmailCredentialsOperator(bpy.types.Operator):
	bl_idname = "render_notify.clear_email_credentials"
	bl_label = "Clear Email Credentials"
	bl_description = "Remove saved email credentials from the system keyring"

	def execute(self, context):
		clear_email_credentials()
		self.report({"INFO"}, "Email credentials cleared.")
		return {"FINISHED"}


class SetDiscordWebhookOperator(bpy.types.Operator):
	bl_idname = "render_notify.set_discord_webhook"
	bl_label = "Set Discord Webhook"
	bl_description = "Save a Discord webhook URL to the system keyring"

	webhook_url: StringProperty(
		name="Webhook URL",
		description="Discord webhook URL (https://discord.com/api/webhooks...)",
	)

	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self, width=520)

	def draw(self, context):
		self.layout.prop(self, "webhook_url")

	def execute(self, context):
		if not self.webhook_url:
			self.report({"ERROR"}, "Webhook URL cannot be empty.")
			return {"CANCELLED"}
		if not self.webhook_url.startswith("https://discord.com/api/webhooks/"):
			self.report({"ERROR"}, "Invalid Discord webhook URL.")
			return {"CANCELLED"}
		set_discord_webhook(self.webhook_url)
		self.report({"INFO"}, "Discord webhook saved.")
		return {"FINISHED"}


class ClearDiscordWebhookOperator(bpy.types.Operator):
	bl_idname = "render_notify.clear_discord_webhook"
	bl_label = "Clear Discord Webhook"
	bl_description = "Remove saved Discord webhook from the system keyring"

	def execute(self, context):
		clear_discord_webhook()
		self.report({"INFO"}, "Discord webhook cleared.")
		return {"FINISHED"}

