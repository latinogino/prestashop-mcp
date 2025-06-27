"""Configuration management for PrestaShop MCP Server."""

import os
from typing import Optional

from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config(BaseModel):
    """Configuration for PrestaShop MCP Server."""
    
    shop_url: str = Field(
        description="PrestaShop shop URL",
        default_factory=lambda: os.getenv("PRESTASHOP_SHOP_URL", "")
    )
    
    api_key: str = Field(
        description="PrestaShop API key",
        default_factory=lambda: os.getenv("PRESTASHOP_API_KEY", "")
    )
    
    log_level: str = Field(
        description="Logging level",
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO")
    )
    
    def validate_config(self) -> None:
        """Validate that required configuration is present."""
        if not self.shop_url:
            raise ValueError("PRESTASHOP_SHOP_URL environment variable is required")
        
        if not self.api_key:
            raise ValueError("PRESTASHOP_API_KEY environment variable is required")
        
        if not self.shop_url.startswith(('http://', 'https://')):
            raise ValueError("PRESTASHOP_SHOP_URL must start with http:// or https://")
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        config = cls()
        config.validate_config()
        return config