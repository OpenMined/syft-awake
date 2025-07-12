"""
Syft Awake - Network awakeness monitoring for SyftBox

Fast, secure awakeness monitoring that allows SyftBox network members to ping 
each other to check if they're online and ready for interactive queries.
"""

__version__ = "0.2.5"

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
    # Try to get network status
    try:
        network_summary = ping_network()
        
        # Generate table rows
        table_rows = ""
        for i, user in enumerate(network_summary.users):
            status_color = "#10b981" if user.is_awake else "#ef4444"
            status_text = "✓ Awake" if user.is_awake else "✗ Offline"
            status_bg = "#dcfce7" if user.is_awake else "#fee2e2"
            country_text = user.country or "Unknown"
            
            table_rows += f"""
                <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 0.75rem 1rem; text-align: center;">{i}</td>
                    <td style="padding: 0.75rem 1rem;">
                        <div style="font-weight: 500; color: #111827;">{user.email}</div>
                    </td>
                    <td style="padding: 0.75rem 1rem;">
                        <span style="display: inline-flex; align-items: center; padding: 0.25rem 0.5rem; background: {status_bg}; color: {status_color}; border-radius: 0.25rem; font-size: 0.75rem; font-weight: 500;">
                            {status_text}
                        </span>
                    </td>
                    <td style="padding: 0.75rem 1rem;">
                        <div style="display: flex; align-items: center; gap: 0.25rem; color: #6b7280;">
                            <svg style="width: 1rem; height: 1rem;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <path d="M2 12h20"></path>
                                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                            </svg>
                            <span>{country_text}</span>
                        </div>
                    </td>
                </tr>
            """
        
        # Generate country summary
        country_badges = ""
        for country, count in network_summary.countries.items():
            country_badges += f"""
                <span style="display: inline-flex; align-items: center; padding: 0.25rem 0.5rem; background: #e5e7eb; border-radius: 0.25rem; font-size: 0.75rem; margin-right: 0.5rem;">
                    {country}: {count}
                </span>
            """
        
        return f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #ffffff;">
            <div style="border: 1px solid #e5e7eb; border-radius: 0.375rem; overflow: hidden;">
                <div style="background: #f3f4f6; padding: 1rem 1.25rem; border-bottom: 1px solid #e5e7eb;">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <h2 style="font-size: 1.125rem; font-weight: 600; color: #111827; margin: 0;">🌐 Syft Awake Network Status</h2>
                            <span style="font-size: 0.75rem; color: #6b7280;">v{__version__}</span>
                        </div>
                        <div style="display: flex; gap: 1rem; align-items: center;">
                            <span style="font-size: 0.875rem; color: #374151;">
                                <strong>{network_summary.awake_count}</strong> of <strong>{network_summary.total_users}</strong> awake
                            </span>
                            <div style="background: #dbeafe; color: #1e40af; padding: 0.25rem 0.75rem; border-radius: 0.25rem; font-size: 0.875rem; font-weight: 500;">
                                {network_summary.awake_percentage:.1f}% Online
                            </div>
                        </div>
                    </div>
                </div>
                
                <div style="overflow-x: auto;">
                    <table style="width: 100%; border-collapse: collapse; font-size: 0.875rem;">
                        <thead>
                            <tr style="background: #f9fafb; border-bottom: 1px solid #e5e7eb;">
                                <th style="padding: 0.75rem 1rem; text-align: left; font-weight: 500; color: #374151; width: 3rem;">#</th>
                                <th style="padding: 0.75rem 1rem; text-align: left; font-weight: 500; color: #374151;">Email</th>
                                <th style="padding: 0.75rem 1rem; text-align: left; font-weight: 500; color: #374151;">Status</th>
                                <th style="padding: 0.75rem 1rem; text-align: left; font-weight: 500; color: #374151;">Location</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows}
                        </tbody>
                    </table>
                </div>
                
                <div style="background: #f9fafb; padding: 1rem 1.25rem; border-top: 1px solid #e5e7eb;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <span style="font-size: 0.75rem; color: #6b7280;">Countries:</span>
                            {country_badges if country_badges else '<span style="font-size: 0.75rem; color: #9ca3af;">Location data not available</span>'}
                        </div>
                        <span style="font-size: 0.75rem; color: #9ca3af;">
                            Fast, secure awakeness monitoring for SyftBox
                        </span>
                    </div>
                </div>
            </div>
        </div>
        """
    except Exception as e:
        # Fallback to simple display if ping_network fails
        return f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #ffffff;">
            <div style="border: 1px solid #e5e7eb; border-radius: 0.375rem; overflow: hidden;">
                <div style="background: #fee2e2; padding: 1rem 1.25rem; text-align: center;">
                    <h3 style="color: #991b1b; margin: 0;">Network Status Unavailable</h3>
                    <p style="color: #7f1d1d; margin-top: 0.5rem; font-size: 0.875rem;">Unable to fetch network status. Please check your SyftBox connection.</p>
                </div>
                <div style="background: #f3f4f6; padding: 1rem 1.25rem; border-top: 1px solid #e5e7eb;">
                    <h3 style="font-size: 1rem; font-weight: 600; color: #111827; margin-bottom: 0.75rem;">Available Functions:</h3>
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <div>
                            <code style="background-color: #e5e7eb; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-family: monospace; font-size: 0.875rem;">ping_user(email)</code>
                            <span style="color: #6b7280; margin-left: 0.5rem;">- Check if a specific user is online</span>
                        </div>
                        <div>
                            <code style="background-color: #e5e7eb; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-family: monospace; font-size: 0.875rem;">ping_network()</code>
                            <span style="color: #6b7280; margin-left: 0.5rem;">- Check status of all network members</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

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