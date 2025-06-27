"""Command line interface for PrestaShop MCP Server."""

import asyncio
import logging
import sys
from typing import Optional

import click

from .config import Config
from .prestashop_mcp_server import main as server_main


def setup_logging(level: str):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stderr)
        ]
    )


@click.command()
@click.option(
    '--shop-url',
    envvar='PRESTASHOP_SHOP_URL',
    help='PrestaShop shop URL'
)
@click.option(
    '--api-key',
    envvar='PRESTASHOP_API_KEY',
    help='PrestaShop API key'
)
@click.option(
    '--log-level',
    envvar='LOG_LEVEL',
    default='INFO',
    help='Logging level'
)
def main(
    shop_url: Optional[str],
    api_key: Optional[str],
    log_level: str
):
    """Start the PrestaShop MCP Server."""
    try:
        # Setup logging
        setup_logging(log_level)
        logger = logging.getLogger(__name__)
        
        # Create configuration
        if shop_url and api_key:
            config = Config(
                shop_url=shop_url,
                api_key=api_key,
                log_level=log_level
            )
        else:
            config = Config.from_env()
        
        config.validate_config()
        
        logger.info(f"Starting PrestaShop MCP Server for shop: {config.shop_url}")
        
        # Run server
        asyncio.run(server_main())
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()