import os
import sys
import types

# Add project root to sys.path so tests can import the package
# We need the parent directory of the package folder on sys.path so
# importing `render_notify` works from tests.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Provide a minimal fake `bpy` module for tests run outside Blender.
try:
    import bpy  # type: ignore
except Exception:
    import types

    bpy_mod = types.ModuleType("bpy")

    # Create submodules for bpy.app and bpy.app.handlers so statements
    # like `from bpy.app.handlers import persistent` work.
    app_mod = types.ModuleType("bpy.app")
    handlers_mod = types.ModuleType("bpy.app.handlers")

    def persistent(fn):
        return fn

    handlers_mod.persistent = persistent
    handlers_mod.render_init = []
    handlers_mod.render_complete = []
    handlers_mod.render_cancel = []

    app_mod.handlers = handlers_mod
    bpy_mod.app = app_mod

    # minimal utils / types / context
    bpy_mod.utils = types.SimpleNamespace(unregister_class=lambda cls: None, register_class=lambda cls: None)
    bpy_mod.types = types.SimpleNamespace(AddonPreferences=object, Operator=object)
    bpy_mod.context = types.SimpleNamespace(preferences=types.SimpleNamespace(addons={}))

    sys.modules["bpy"] = bpy_mod
    sys.modules["bpy.app"] = app_mod
    sys.modules["bpy.app.handlers"] = handlers_mod

# Provide a minimal fake `keyring` module so core/keyring_store can be imported
try:
    import keyring  # type: ignore
except Exception:
    keyring_mod = types.ModuleType("keyring")

    class _Errors:
        class PasswordDeleteError(Exception):
            pass

    keyring_mod.errors = _Errors

    def _get_password(service, key):
        return None

    def _set_password(service, key, value):
        return None

    def _delete_password(service, key):
        raise _Errors.PasswordDeleteError()

    keyring_mod.get_password = _get_password
    keyring_mod.set_password = _set_password
    keyring_mod.delete_password = _delete_password

    sys.modules["keyring"] = keyring_mod

# Make package placeholders for relative imports when loading modules directly
try:
    import render_notify  # type: ignore
except Exception:
    pkg = types.ModuleType("render_notify")
    pkg.__path__ = [ROOT]
    sys.modules["render_notify"] = pkg

try:
    import render_notify.core  # type: ignore
except Exception:
    core_pkg = types.ModuleType("render_notify.core")
    core_pkg.__path__ = [os.path.join(ROOT, "render_notify", "core")]
    sys.modules["render_notify.core"] = core_pkg
