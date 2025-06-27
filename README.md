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

### 📦 Product Management
- `get_products` - Retrieve and filter products
- `create_product` - Create new products (with inventory, reference, weight)
- `update_product` - Fully edit products
- `delete_product` - Remove products
- `update_product_stock` - Manage inventory levels
- `update_product_price` - Update prices and wholesale prices

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

### 🏗️ Development Environment

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

Add this configuration to `claude_desktop_config.json`:

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
# With environment variables
prestashop-mcp

# With direct parameters
prestashop-mcp --shop-url https://your-shop.com --api-key YOUR_API_KEY

# Debug mode
prestashop-mcp --log-level DEBUG
```

### 🧪 Testing

```bash
# Run comprehensive CRUD tests
python tests/test_crud_operations.py

# Run unit tests
pytest

# Run tests with coverage
pytest --cov=src/prestashop_mcp --cov-report=html
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
- **[GitHub Repository](https://github.com/your-username/prestashop-mcp)**

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 📝 Changelog

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
