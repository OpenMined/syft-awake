"""
Syft Awake - Network awakeness monitoring for SyftBox

Fast, secure awakeness monitoring that allows SyftBox network members to ping 
each other to check if they're online and ready for interactive queries.
"""

__version__ = "0.1.1"

# Import main functions for easy access
from .client import ping_user, ping_network, is_awake, get_awake_users
from .models import AwakeRequest, AwakeResponse, AwakeStatus

__all__ = [
    "ping_user",
    "ping_network", 
    "is_awake",
    "get_awake_users",
    "AwakeRequest",
    "AwakeResponse", 
    "AwakeStatus",
]