"""
Syft Awake - Network awakeness monitoring for SyftBox

Fast, secure awakeness monitoring that allows SyftBox network members to ping 
each other to check if they're online and ready for interactive queries.
"""

__version__ = "0.2.4"

# Auto-install as SyftBox app if SyftBox is available
try:
    import importlib
    _auto_mod = importlib.import_module('.auto_install', package=__name__)
    _auto_mod.auto_install()
    del importlib, _auto_mod
except Exception:
    pass

# Import core functions only - use importlib to avoid namespace pollution
import importlib as _importlib
_client_mod = _importlib.import_module('.client', package=__name__)

ping_user = _client_mod.ping_user
ping_network = _client_mod.ping_network

del _importlib, _client_mod

__all__ = [
    "ping_user",
    "ping_network",
]

# Add _repr_html_ for Jupyter notebook display
def _repr_html_():
    """Display HTML representation of syft_awake module in Jupyter notebooks."""
    return """
    <div style="border: 2px solid #007ACC; border-radius: 8px; padding: 20px; background-color: #f0f8ff; font-family: Arial, sans-serif;">
        <h2 style="color: #007ACC; margin-top: 0;">🌐 Syft Awake v{version}</h2>
        <p style="color: #333; font-size: 16px;">Network awakeness monitoring for SyftBox</p>
        <div style="margin-top: 15px;">
            <h3 style="color: #005999;">Available Functions:</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin: 8px 0;">
                    <code style="background-color: #e8f4f8; padding: 4px 8px; border-radius: 4px;">ping_user(email)</code> 
                    - Check if a specific user is online
                </li>
                <li style="margin: 8px 0;">
                    <code style="background-color: #e8f4f8; padding: 4px 8px; border-radius: 4px;">ping_network()</code> 
                    - Check status of all network members
                </li>
            </ul>
        </div>
        <div style="margin-top: 15px; font-size: 14px; color: #666;">
            <em>Fast, secure awakeness monitoring for the SyftBox network</em>
        </div>
    </div>
    """.format(version=__version__)

import sys as _sys
_this_module = _sys.modules[__name__]
_this_module._repr_html_ = _repr_html_

# Clean up namespace completely
_all_names = list(globals().keys())
for _name in _all_names:
    if _name not in __all__ and not _name.startswith('_') and _name not in ['__doc__', '__file__', '__name__', '__package__', '__path__', '__spec__', '__version__', '_repr_html_']:
        try:
            delattr(_this_module, _name)
        except (AttributeError, ValueError):
            pass
del _sys, _this_module, _all_names, _name