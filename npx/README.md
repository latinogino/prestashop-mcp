# PrestaShop MCP NPX Wrapper

This NPX wrapper allows you to use the PrestaShop MCP Python server through NPX/Node.js.

## Installation

### Global Installation
```bash
cd npx
npm install -g .
```

### Local Usage (without installation)
```bash
cd npx
npm install
npx . --shop-url "https://shop.ginos.cloud" --api-key "YOUR_API_KEY"
```

## Usage

### Command Line
```bash
# After global installation
prestashop-mcp --shop-url "https://shop.ginos.cloud" --api-key "YOUR_API_KEY"

# With NPX (without installation)
npx prestashop-mcp-npx --shop-url "https://shop.ginos.cloud" --api-key "YOUR_API_KEY"
```

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "prestashop-ultra": {
      "command": "npx",
      "args": ["prestashop-mcp"],
      "env": {
        "PRESTASHOP_SHOP_URL": "https://shop.ginos.cloud",
        "PRESTASHOP_API_KEY": "YOUR_API_KEY",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### With Local Python Installation

If you have the Python version cloned locally:

```bash
prestashop-mcp --python-path "/path/to/prestashop-mcp/src" --shop-url "https://shop.ginos.cloud" --api-key "YOUR_API_KEY"
```

## Options

- `--shop-url <url>` - PrestaShop shop URL
- `--api-key <key>` - PrestaShop API key  
- `--log-level <level>` - Logging level (default: INFO)
- `--python-path <path>` - Path to Python prestashop-mcp installation
- `--help` - Show help

## Requirements

- Node.js 18+
- Python 3.8+
- PrestaShop MCP Python package (installed or available locally)

## Troubleshooting

### Python not found
Ensure Python is installed and available in PATH:
```bash
python --version
# or
python3 --version
```

### PrestaShop MCP module not found
1. Install the Python package: `pip install prestashop-mcp`
2. Or use `--python-path` to point to local installation
3. Or run from the repository root where `src/` is available

### NPX command not found
Ensure the package is installed globally:
```bash
npm install -g .
```