"""
Location detection service for syft-awake using IP geolocation.
"""

import json
from typing import Optional
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from loguru import logger

__all__ = [
    "detect_country",
]


def detect_country(enabled: bool = True, timeout: int = 5) -> Optional[str]:
    """
    Detect the country of the current node based on its public IP address.
    
    Args:
        enabled: Whether location detection is enabled (default: True)
        timeout: Timeout in seconds for the HTTP request (default: 5)
        
    Returns:
        ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB', 'DE') or None if detection fails
    """
    if not enabled:
        logger.debug("Location detection is disabled")
        return None
        
    try:
        # Use country.is API - free, no authentication required
        with urlopen("https://api.country.is/", timeout=timeout) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                country_code = data.get('country')
                if country_code:
                    logger.debug(f"Detected country: {country_code}")
                    return country_code
                else:
                    logger.warning("Country detection returned empty result")
                    return None
            else:
                logger.warning(f"Country detection API returned status {response.status}")
                return None
                
    except HTTPError as e:
        logger.warning(f"HTTP error during country detection: {e}")
        return None
    except URLError as e:
        logger.warning(f"Network error during country detection: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON response during country detection: {e}")
        return None
    except Exception as e:
        logger.warning(f"Unexpected error during country detection: {e}")
        return None