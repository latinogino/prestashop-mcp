# PrestaShop MCP Server

A professional Model Context Protocol (MCP) Server for complete management of PrestaShop e-commerce stores.

## 🚀 Overview

This MCP Server enables complete management of your PrestaShop store through AI applications like Claude Desktop. With specialized tools, you can manage all aspects of your e-commerce business - from products and categories to customers and orders.

## ✨ Features

- **🛍️ Complete Store Management** - Tools for all e-commerce areas
- **🏗️ MCP Protocol Compliance** for seamless AI integration
- **⚡ Async/Await Architecture** for maximum performance
- **🛡️ Comprehensive Error Handling** and validation
- **🔧 Production-Ready** with complete test suite
- **📖 Comprehensive Documentation** with practical examples

## 🛠️ Available Tools

### 📦 Unified Product Management
- `get_products` - **UNIFIED** Product retrieval supporting all use cases:
  - **Single Product by ID**: Complete product details including stock and category info
  - **Multiple Products**: List with optional filtering and enhancement
  - **Flexible Enhancement**: Optional stock info, category details, custom field selection
  - **Smart Filtering**: By category, name, or custom criteria

### 🏷️ Category Management
- `get_categories` - Retrieve categories (with hierarchy filter)
- `create_category` - Create new categories
- `update_category` - Edit categories
- `delete_category` - Remove categories

### 👥 Customer Management
- `get_customers` - Retrieve and filter customers
- `create_customer` - Create new customers
- `update_customer` - Edit customer data

### 📋 Order Management
- `get_orders` - Retrieve and filter orders
- `update_order_status` - Change order status
- `get_order_states` - Retrieve available statuses

### ⚙️ Store Administration
- `test_connection` - Test API connection
- `get_shop_info` - Comprehensive store statistics

## 📋 Installation

### ⚠️ Recommended Installation (Virtual Environment)

**This approach prevents module conflicts and ensures reliable installation:**

#### Windows:
```powershell
# Clone repository
git clone https://github.com/latinogino/prestashop-mcp.git
cd prestashop-mcp

# Create virtual environment
python -m venv venv_prestashop

# Activate virtual environment
.\venv_prestashop\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .

# Verify installation
python -c "import prestashop_mcp; print('✅ Installation successful')"

# Note the Python path for Claude Desktop configuration
Write-Host "Python Path: $((Get-Command python).Source)"
```

#### Linux/macOS:
```bash
# Clone repository
git clone https://github.com/latinogino/prestashop-mcp.git
cd prestashop-mcp

# Create virtual environment
python3 -m venv venv_prestashop

# Activate virtual environment
source venv_prestashop/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .

# Verify installation
python -c "import prestashop_mcp; print('✅ Installation successful')"

# Note the Python path for Claude Desktop configuration
which python
```

### 🏗️ Alternative: System-wide Installation

```bash
# Clone repository
git clone https://github.com/latinogino/prestashop-mcp.git
cd prestashop-mcp

# Install dependencies (includes test dependencies)
pip install -r requirements.txt

# Install package
pip install -e .
```

### ⚙️ Configuration

Create a `.env` file based on `.env.example`:

```bash
# PrestaShop Configuration
PRESTASHOP_SHOP_URL=https://your-shop.example.com
PRESTASHOP_API_KEY=YOUR_API_KEY

# Logging
LOG_LEVEL=INFO
```

## 🎯 Usage

### 🤖 With Claude Desktop

#### Using Virtual Environment (Recommended)

Add this configuration to `claude_desktop_config.json`:

**Windows:**
```json
{
  "mcpServers": {
    "prestashop": {
      "command": "C:\\\\path\\\\to\\\\prestashop-mcp\\\\venv_prestashop\\\\Scripts\\\\python.exe",
      "args": ["-m", "prestashop_mcp.prestashop_mcp_server"],
      "cwd": "C:\\\\path\\\\to\\\\prestashop-mcp",
      "env": {
        "PRESTASHOP_SHOP_URL": "https://your-shop.example.com",
        "PRESTASHOP_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

**Linux/macOS:**
```json
{
  "mcpServers": {
    "prestashop": {
      "command": "/path/to/prestashop-mcp/venv_prestashop/bin/python",
      "args": ["-m", "prestashop_mcp.prestashop_mcp_server"],
      "cwd": "/path/to/prestashop-mcp",
      "env": {
        "PRESTASHOP_SHOP_URL": "https://your-shop.example.com",
        "PRESTASHOP_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

#### Using System Python (Alternative)

```json
{
  "mcpServers": {
    "prestashop": {
      "command": "python",
      "args": ["-m", "prestashop_mcp.prestashop_mcp_server"],
      "cwd": "/path/to/prestashop-mcp",
      "env": {
        "PRESTASHOP_SHOP_URL": "https://your-shop.example.com",
        "PRESTASHOP_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### 💻 CLI Usage

```bash
# Activate virtual environment first (if using venv)
source venv_prestashop/bin/activate  # Linux/macOS
.\venv_prestashop\Scripts\Activate.ps1  # Windows

# With environment variables
prestashop-mcp

# With direct parameters
prestashop-mcp --shop-url https://your-shop.com --api-key YOUR_API_KEY

# Debug mode
prestashop-mcp --log-level DEBUG
```

### 🧪 Testing

```bash
# Activate virtual environment first (if using venv)
source venv_prestashop/bin/activate  # Linux/macOS
.\venv_prestashop\Scripts\Activate.ps1  # Windows

# Run comprehensive CRUD tests
python tests/test_crud_operations.py

# Run unit tests
pytest

# Run tests with coverage
pytest --cov=src/prestashop_mcp --cov-report=html
```

## 🆕 Unified Product API

The `get_products` tool now handles **all product retrieval scenarios** with a single, powerful interface:

### **Single Product Retrieval**
```
"Get complete details for product ID 15 including stock and category information"
```

### **Product Lists with Enhancement**
```
"Get all products in category 5 with stock information"
```

### **Flexible Field Selection**
```
"Get products showing only ID, name, and price fields"
```

### **Smart Filtering**
```
"Find products containing 'laptop' in the name with full details"
```

### **Use Cases:**

| Scenario | Parameters | Result |
|----------|------------|--------|
| **Single Product Details** | `product_id="15", include_stock=true, include_category_info=true` | Complete product info with stock & category |
| **Product List** | `limit=20, category_id="5"` | List of products in category 5 |
| **Enhanced List** | `limit=10, include_details=true, include_stock=true` | Full product details with stock for 10 products |
| **Filtered Search** | `name_filter="laptop", include_details=true` | All laptop products with complete information |
| **Custom Fields** | `display="id,name,price", limit=50` | Specific fields only for 50 products |

## 🔧 Troubleshooting

### ❌ Common Issues

#### "ModuleNotFoundError: No module named 'prestashop_mcp'"

**Solution:** Use virtual environment and ensure package is installed:
```bash
# Check if in virtual environment
python -c "import sys; print(sys.prefix)"

# Reinstall package
pip install -e .

# Verify installation
python -c "import prestashop_mcp; print('Module found')"
```

#### Claude Desktop Connection Issues

1. **Check Python Path:** Ensure the `command` path in `claude_desktop_config.json` points to the correct Python executable
2. **Check Working Directory:** Ensure `cwd` points to the prestashop-mcp directory
3. **Check Environment Variables:** Verify `PRESTASHOP_SHOP_URL` and `PRESTASHOP_API_KEY` are correct

#### API Connection Issues

Test your PrestaShop API connection:
```bash
curl -u "YOUR_API_KEY:" https://your-shop.com/api/configurations?output_format=JSON
```

### 🔍 Debug Mode

Enable debug logging in Claude Desktop configuration:
```json
{
  "mcpServers": {
    "prestashop": {
      "command": "path/to/python",
      "args": ["-m", "prestashop_mcp.prestashop_mcp_server"],
      "cwd": "path/to/prestashop-mcp",
      "env": {
        "PRESTASHOP_SHOP_URL": "https://your-shop.example.com",
        "PRESTASHOP_API_KEY": "YOUR_API_KEY",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

## 📊 Project Structure

```
prestashop-mcp/
├── src/prestashop_mcp/                  # Main Package
│   ├── prestashop_mcp_server.py         # MCP Server
│   ├── prestashop_client.py             # PrestaShop API Client
│   ├── config.py                        # Configuration Management
│   └── cli.py                          # Command Line Interface
├── tests/                               # All Tests
│   ├── test_config.py                   # Unit Tests
│   └── test_crud_operations.py          # CRUD Integration Tests
├── venv_prestashop/                     # Virtual Environment (after setup)
├── README.md                            # Documentation
├── pyproject.toml                       # Package Configuration
└── requirements.txt                     # All Dependencies
```

## 📖 API Documentation

### PrestaShop API

Complete PrestaShop API documentation:
- **[PrestaShop DevDocs - Webservice](https://devdocs.prestashop-project.org/8/webservice/)**

### Authentication

```bash
curl -u "API_KEY:" https://your-shop.com/api/configurations?output_format=JSON
```

### Important Endpoints

- **Products**: `/api/products`
- **Categories**: `/api/categories`
- **Customers**: `/api/customers`
- **Orders**: `/api/orders`
- **Stock**: `/api/stock_availables`
- **Order Status**: `/api/order_states`

## 🧪 Development

### 🏗️ Development Environment

```bash
# Activate virtual environment
source venv_prestashop/bin/activate  # Linux/macOS
.\venv_prestashop\Scripts\Activate.ps1  # Windows

# All dependencies (including test dependencies) are in requirements.txt
pip install -r requirements.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=src/prestashop_mcp --cov-report=html

# Run comprehensive integration tests
python tests/test_crud_operations.py
```

## 📖 Resources

- **[PrestaShop Official Documentation](https://devdocs.prestashop-project.org/)**
- **[Model Context Protocol Specification](https://modelcontextprotocol.io/)**
- **[Claude Desktop MCP Integration](https://docs.anthropic.com/)**
- **[GitHub Repository](https://github.com/latinogino/prestashop-mcp)**

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 📝 Changelog

### v2.0.0 - Unified Product API (BREAKING CHANGES)
- ✨ **MAJOR**: Unified `get_products` API handles all product retrieval scenarios
- 🗑️ **REMOVED**: `get_product_details` method (functionality merged into `get_products`)
- 🔧 **Enhanced**: Single API call for both individual products and lists
- 📊 **Flexible**: Optional enhancement with stock, category, and custom field selection
- 🏗️ **Cleaner**: Eliminates API duplication and provides intuitive interface
- 🎯 **Breaking**: Update your integrations to use the new unified `get_products` method

### v1.1.0 - Enhanced Product Details
- ✨ **NEW**: `get_product_details` method for comprehensive product information
- 📊 Enhanced product queries with stock and category information
- 🔍 Flexible field selection with display parameter
- 🏗️ Improved API client architecture for detailed data retrieval

### v1.0.1 - Improved Installation
- 📖 Enhanced installation documentation with virtual environment setup
- 🔧 Added comprehensive troubleshooting section
- 🎯 Platform-specific installation instructions (Windows/Linux/macOS)
- ⚡ Improved Claude Desktop configuration examples

### v1.0.0 - Production Release
- ✨ Complete store management with professional tools
- 📦 Enhanced product features (inventory, prices, references)
- 🏷️ Category management with hierarchy support
- 👥 Customer management (create, edit)
- 📋 Order management with status updates
- ⚙️ Store statistics and configuration
- 🛡️ Production-ready with comprehensive tests
- 📖 Complete documentation with practical examples

---

**🎯 Manage your complete PrestaShop through natural language with Claude Desktop!**
