"""Backwards compatible access point for application settings.

The project historically imported :mod:`app.shared.settings`; this module now
re-exports the settings defined under :mod:`app.core.config` to avoid touching
every import while enabling the new configuration layer.
"""

from app.core.config import DGIIEnvironment, Settings, get_settings, settings

__all__ = ["DGIIEnvironment", "Settings", "get_settings", "settings"]
