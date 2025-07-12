"""
Unit tests for location-related model functionality.
"""

import pytest
from datetime import datetime, timezone
import sys
from pathlib import Path

# Add src to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from syft_awake.models import AwakeResponse, AwakeStatus, NetworkAwakenessSummary


class TestAwakeResponseLocation:
    """Test location functionality in AwakeResponse model."""
    
    def test_awake_response_with_country(self):
        """Test AwakeResponse with country field."""
        response = AwakeResponse(
            responder="test@example.com",
            status=AwakeStatus.AWAKE,
            message="I'm awake!",
            country="US"
        )
        
        assert response.country == "US"
        assert response.responder == "test@example.com"
        assert response.status == AwakeStatus.AWAKE
    
    def test_awake_response_without_country(self):
        """Test AwakeResponse without country field (default None)."""
        response = AwakeResponse(
            responder="test@example.com",
            status=AwakeStatus.AWAKE,
            message="I'm awake!"
        )
        
        assert response.country is None
    
    def test_awake_response_country_validation(self):
        """Test that country field accepts valid ISO codes."""
        valid_codes = ["US", "GB", "DE", "FR", "JP", "AU", "CA", "IN", "BR"]
        
        for code in valid_codes:
            response = AwakeResponse(
                responder="test@example.com",
                status=AwakeStatus.AWAKE,
                message="I'm awake!",
                country=code
            )
            assert response.country == code
    
    def test_awake_response_json_serialization(self):
        """Test JSON serialization includes country field."""
        response = AwakeResponse(
            responder="test@example.com",
            status=AwakeStatus.AWAKE,
            message="I'm awake!",
            country="GB"
        )
        
        json_data = response.model_dump()
        assert "country" in json_data
        assert json_data["country"] == "GB"
    
    def test_awake_response_json_serialization_none_country(self):
        """Test JSON serialization with None country."""
        response = AwakeResponse(
            responder="test@example.com",
            status=AwakeStatus.AWAKE,
            message="I'm awake!"
        )
        
        json_data = response.model_dump()
        assert "country" in json_data
        assert json_data["country"] is None


class TestNetworkAwakenessSummaryLocation:
    """Test location functionality in NetworkAwakenessSummary model."""
    
    def test_network_summary_with_countries(self):
        """Test NetworkAwakenessSummary with country distribution."""
        summary = NetworkAwakenessSummary(
            total_pinged=5,
            awake_count=3,
            response_count=4,
            awake_users=["user1@example.com", "user2@example.com", "user3@example.com"],
            sleeping_users=["user4@example.com"],
            non_responsive=["user5@example.com"],
            scan_duration_ms=1500.0,
            countries={"US": 2, "GB": 1}
        )
        
        assert summary.countries == {"US": 2, "GB": 1}
        assert summary.total_pinged == 5
        assert summary.awake_count == 3
    
    def test_network_summary_empty_countries(self):
        """Test NetworkAwakenessSummary with empty countries (default)."""
        summary = NetworkAwakenessSummary(
            total_pinged=2,
            awake_count=0,
            response_count=0,
            awake_users=[],
            sleeping_users=[],
            non_responsive=["user1@example.com", "user2@example.com"],
            scan_duration_ms=500.0
        )
        
        assert summary.countries == {}
    
    def test_network_summary_countries_json_serialization(self):
        """Test JSON serialization includes countries field."""
        summary = NetworkAwakenessSummary(
            total_pinged=3,
            awake_count=3,
            response_count=3,
            awake_users=["user1@example.com", "user2@example.com", "user3@example.com"],
            sleeping_users=[],
            non_responsive=[],
            scan_duration_ms=800.0,
            countries={"DE": 1, "FR": 1, "IT": 1}
        )
        
        json_data = summary.model_dump()
        assert "countries" in json_data
        assert json_data["countries"] == {"DE": 1, "FR": 1, "IT": 1}
    
    def test_network_summary_properties_with_countries(self):
        """Test that existing properties still work with countries field."""
        summary = NetworkAwakenessSummary(
            total_pinged=4,
            awake_count=2,
            response_count=3,
            awake_users=["user1@example.com", "user2@example.com"],
            sleeping_users=["user3@example.com"],
            non_responsive=["user4@example.com"],
            scan_duration_ms=1200.0,
            countries={"US": 1, "CA": 1}
        )
        
        # Test existing properties still work
        assert summary.awakeness_ratio == 0.5  # 2/4
        assert summary.response_ratio == 0.75  # 3/4
        
        # Test new countries field
        assert summary.countries == {"US": 1, "CA": 1}
    
    def test_network_summary_large_country_distribution(self):
        """Test NetworkAwakenessSummary with many countries."""
        countries = {
            "US": 10, "GB": 5, "DE": 3, "FR": 2, "JP": 1,
            "AU": 4, "CA": 6, "IN": 8, "BR": 2, "NL": 1
        }
        
        summary = NetworkAwakenessSummary(
            total_pinged=50,
            awake_count=42,
            response_count=45,
            awake_users=[f"user{i}@example.com" for i in range(42)],
            sleeping_users=[f"sleep{i}@example.com" for i in range(3)],
            non_responsive=[f"offline{i}@example.com" for i in range(5)],
            scan_duration_ms=5000.0,
            countries=countries
        )
        
        assert summary.countries == countries
        assert len(summary.countries) == 10
        assert sum(summary.countries.values()) == 42  # Should match awake_count


if __name__ == "__main__":
    pytest.main([__file__])