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
    enable_discord: BoolProperty(
        name="Enable Discord Notifications",
        default=False,
    )

    def draw(self, context):
        layout = self.layout

        # ── Email ──────────────────────────────────────────────────────────────
        box = layout.box()
        box.prop(self, "enable_email")
        if self.enable_email:
            row = box.row()
            row.prop(self, "smtp_host")
            row.prop(self, "smtp_port")

            email, _ = get_email_credentials()
            if email:
                box.label(text=f"Logged in as: {email}", icon="CHECKMARK")
                box.operator(
                    "render_notify.clear_email_credentials",
                    text="Clear Email Credentials",
                    icon="X",
                )
            else:
                box.label(text="No credentials set.", icon="ERROR")
                box.operator(
                    "render_notify.set_email_credentials",
                    text="Set Email Credentials",
                    icon="PLUS",
                )

        # ── Discord ────────────────────────────────────────────────────────────
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
    bl_description = "Save Gmail address and App Password to the system keyring"

    email: StringProperty(name="Email", description="Your Gmail address")
    password: StringProperty(
        name="App Password",
        description="Gmail App Password (not your main account password)",
        subtype="PASSWORD",
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=420)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "email")
        layout.prop(self, "password")
        layout.label(
            text="Use a Gmail App Password, not your account password.",
            icon="INFO",
        )

    def execute(self, context):
        if not self.email or not self.password:
            self.report({"ERROR"}, "Email and password cannot be empty.")
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
        description="Discord webhook URL (https://discord.com/api/webhooks/...)",
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

