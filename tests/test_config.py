"""Tests for PrestaShop MCP configuration."""

import os
import pytest
from unittest.mock import patch

from src.prestashop_mcp.config import Config


class TestConfig:
    """Test configuration management."""
    
    def test_config_from_env_success(self):
        """Test successful configuration creation from environment."""
        with patch.dict(os.environ, {
            'PRESTASHOP_SHOP_URL': 'https://test-shop.example.com',
            'PRESTASHOP_API_KEY': 'test-api-key-123',
            'LOG_LEVEL': 'DEBUG'
        }):
            config = Config.from_env()
            assert config.shop_url == 'https://test-shop.example.com'
            assert config.api_key == 'test-api-key-123'
            assert config.log_level == 'DEBUG'
    
    def test_config_validation_missing_shop_url(self):
        """Test validation fails when shop URL is missing."""
        config = Config(shop_url="", api_key="test-key")
        with pytest.raises(ValueError, match="PRESTASHOP_SHOP_URL environment variable is required"):
            config.validate_config()
    
    def test_config_validation_missing_api_key(self):
        """Test validation fails when API key is missing."""
        config = Config(shop_url="https://test.com", api_key="")
        with pytest.raises(ValueError, match="PRESTASHOP_API_KEY environment variable is required"):
            config.validate_config()
    
    def test_config_validation_invalid_url(self):
        """Test validation fails when URL is invalid."""
        config = Config(shop_url="invalid-url", api_key="test-key")
        with pytest.raises(ValueError, match="PRESTASHOP_SHOP_URL must start with http:// or https://"):
            config.validate_config()
    
    def test_config_validation_success(self):
        """Test successful validation."""
        config = Config(
            shop_url="https://test-shop.example.com",
            api_key="test-api-key-123"
        )
        # Should not raise any exception
        config.validate_config()