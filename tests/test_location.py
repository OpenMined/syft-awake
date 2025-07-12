"""
Unit tests for location detection functionality.
"""

import pytest
from unittest.mock import patch, mock_open
from urllib.error import URLError, HTTPError
import json
import sys
from pathlib import Path

# Add src to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from syft_awake.location import detect_country


class TestLocationDetection:
    """Test location detection functionality."""
    
    def test_detect_country_disabled(self):
        """Test that location detection returns None when disabled."""
        result = detect_country(enabled=False)
        assert result is None
    
    @patch('syft_awake.location.urlopen')
    def test_detect_country_success(self, mock_urlopen):
        """Test successful country detection."""
        # Mock successful API response
        mock_response = mock_open()
        mock_response.return_value.status = 200
        mock_response.return_value.read.return_value = b'{"country": "US"}'
        mock_response.return_value.__enter__.return_value = mock_response.return_value
        mock_urlopen.return_value = mock_response.return_value
        
        result = detect_country(enabled=True)
        assert result == "US"
        
        # Verify API was called correctly
        mock_urlopen.assert_called_once_with("https://api.country.is/", timeout=5)
    
    @patch('syft_awake.location.urlopen')
    def test_detect_country_empty_response(self, mock_urlopen):
        """Test handling of empty country in response."""
        # Mock API response with empty country
        mock_response = mock_open()
        mock_response.return_value.status = 200
        mock_response.return_value.read.return_value = b'{"country": ""}'
        mock_response.return_value.__enter__.return_value = mock_response.return_value
        mock_urlopen.return_value = mock_response.return_value
        
        result = detect_country(enabled=True)
        assert result is None
    
    @patch('syft_awake.location.urlopen')
    def test_detect_country_missing_country_field(self, mock_urlopen):
        """Test handling of missing country field in response."""
        # Mock API response without country field
        mock_response = mock_open()
        mock_response.return_value.status = 200
        mock_response.return_value.read.return_value = b'{"other_field": "value"}'
        mock_response.return_value.__enter__.return_value = mock_response.return_value
        mock_urlopen.return_value = mock_response.return_value
        
        result = detect_country(enabled=True)
        assert result is None
    
    @patch('syft_awake.location.urlopen')
    def test_detect_country_http_error(self, mock_urlopen):
        """Test handling of HTTP errors."""
        mock_urlopen.side_effect = HTTPError(
            url="https://api.country.is/",
            code=500,
            msg="Internal Server Error",
            hdrs=None,
            fp=None
        )
        
        result = detect_country(enabled=True)
        assert result is None
    
    @patch('syft_awake.location.urlopen')
    def test_detect_country_url_error(self, mock_urlopen):
        """Test handling of network errors."""
        mock_urlopen.side_effect = URLError("Network unreachable")
        
        result = detect_country(enabled=True)
        assert result is None
    
    @patch('syft_awake.location.urlopen')
    def test_detect_country_invalid_json(self, mock_urlopen):
        """Test handling of invalid JSON response."""
        # Mock API response with invalid JSON
        mock_response = mock_open()
        mock_response.return_value.status = 200
        mock_response.return_value.read.return_value = b'invalid json{'
        mock_response.return_value.__enter__.return_value = mock_response.return_value
        mock_urlopen.return_value = mock_response.return_value
        
        result = detect_country(enabled=True)
        assert result is None
    
    @patch('syft_awake.location.urlopen')
    def test_detect_country_non_200_status(self, mock_urlopen):
        """Test handling of non-200 HTTP status codes."""
        # Mock API response with 404 status
        mock_response = mock_open()
        mock_response.return_value.status = 404
        mock_response.return_value.__enter__.return_value = mock_response.return_value
        mock_urlopen.return_value = mock_response.return_value
        
        result = detect_country(enabled=True)
        assert result is None
    
    @patch('syft_awake.location.urlopen')
    def test_detect_country_custom_timeout(self, mock_urlopen):
        """Test that custom timeout is passed correctly."""
        # Mock successful API response
        mock_response = mock_open()
        mock_response.return_value.status = 200
        mock_response.return_value.read.return_value = b'{"country": "GB"}'
        mock_response.return_value.__enter__.return_value = mock_response.return_value
        mock_urlopen.return_value = mock_response.return_value
        
        result = detect_country(enabled=True, timeout=10)
        assert result == "GB"
        
        # Verify custom timeout was used
        mock_urlopen.assert_called_once_with("https://api.country.is/", timeout=10)
    
    @patch('syft_awake.location.urlopen')
    def test_detect_country_unexpected_exception(self, mock_urlopen):
        """Test handling of unexpected exceptions."""
        mock_urlopen.side_effect = Exception("Unexpected error")
        
        result = detect_country(enabled=True)
        assert result is None
    
    @patch('syft_awake.location.urlopen')
    def test_detect_country_various_country_codes(self, mock_urlopen):
        """Test detection of various country codes."""
        test_countries = ["US", "GB", "DE", "FR", "JP", "AU", "CA"]
        
        for country_code in test_countries:
            # Mock API response for each country
            mock_response = mock_open()
            mock_response.return_value.status = 200
            mock_response.return_value.read.return_value = json.dumps({"country": country_code}).encode()
            mock_response.return_value.__enter__.return_value = mock_response.return_value
            mock_urlopen.return_value = mock_response.return_value
            
            result = detect_country(enabled=True)
            assert result == country_code


if __name__ == "__main__":
    pytest.main([__file__])