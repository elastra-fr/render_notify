import keyring

SERVICE = "blender_render_notify"


def get_email_credentials():
	email = keyring.get_password(SERVICE, "email")
	password = keyring.get_password(SERVICE, "password")
	return email, password


def set_email_credentials(email, password):
	keyring.set_password(SERVICE, "email", email)
	keyring.set_password(SERVICE, "password", password)


def clear_email_credentials():
	for key in ("email", "password"):
		try:
			keyring.delete_password(SERVICE, key)
		except keyring.errors.PasswordDeleteError:
			pass


def get_discord_webhook():
	return keyring.get_password(SERVICE, "discord_webhook")


def set_discord_webhook(url):
	keyring.set_password(SERVICE, "discord_webhook", url)


def clear_discord_webhook():
	try:
		keyring.delete_password(SERVICE, "discord_webhook")
	except keyring.errors.PasswordDeleteError:
		pass

