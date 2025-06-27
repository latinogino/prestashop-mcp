# PrestaShop MCP Server

Ein professioneller Model Context Protocol (MCP) Server für die vollständige Verwaltung von PrestaShop E-Commerce Shops.

## 🚀 Überblick

Dieser MCP Server ermöglicht die vollständige Verwaltung Ihres PrestaShop Shops über AI-Anwendungen wie Claude Desktop. Mit spezialisierten Tools können Sie alle Aspekte Ihres E-Commerce-Geschäfts verwalten - von Produkten und Kategorien bis hin zu Kunden und Bestellungen.

## ✨ Features

- **🛍️ Vollständige Shop-Verwaltung** - Tools für alle E-Commerce-Bereiche
- **🏗️ MCP Protocol Compliance** für nahtlose AI-Integration
- **⚡ Async/Await Architektur** für höchste Performance
- **🛡️ Umfassende Fehlerbehandlung** und Validierung
- **🔧 Production-Ready** mit vollständiger Test-Suite
- **📖 Umfassende Dokumentation** mit praktischen Beispielen

## 🛠️ Verfügbare Tools

### 📦 Produkt-Management
- `get_products` - Produkte abrufen und filtern
- `create_product` - Neue Produkte erstellen (mit Lager, Referenz, Gewicht)
- `update_product` - Produkte vollständig bearbeiten
- `delete_product` - Produkte entfernen
- `update_product_stock` - Lagerbestände verwalten
- `update_product_price` - Preise und Einkaufspreise aktualisieren

### 🏷️ Kategorie-Management
- `get_categories` - Kategorien abrufen (mit Hierarchie-Filter)
- `create_category` - Neue Kategorien erstellen
- `update_category` - Kategorien bearbeiten
- `delete_category` - Kategorien entfernen

### 👥 Kunden-Management
- `get_customers` - Kunden abrufen und filtern
- `create_customer` - Neue Kunden anlegen
- `update_customer` - Kundendaten bearbeiten

### 📋 Bestell-Management
- `get_orders` - Bestellungen abrufen und filtern
- `update_order_status` - Bestellstatus ändern
- `get_order_states` - Verfügbare Status abrufen

### ⚙️ Shop-Verwaltung
- `test_connection` - API-Verbindung testen
- `get_shop_info` - Umfassende Shop-Statistiken

## 📋 Installation

### 🏗️ Entwicklungsumgebung

```bash
# Repository klonen
git clone https://github.com/latinogino/prestashop-mcp.git
cd prestashop-mcp

# Dependencies installieren
pip install -r requirements.txt

# Package installieren
pip install -e .
```

### ⚙️ Konfiguration

Erstellen Sie eine `.env` Datei basierend auf `.env.example`:

```bash
# PrestaShop Configuration
PRESTASHOP_SHOP_URL=https://ihr-shop.example.com
PRESTASHOP_API_KEY=IHR_API_KEY

# Logging
LOG_LEVEL=INFO
```

## 🎯 Verwendung

### 🤖 Mit Claude Desktop

Fügen Sie diese Konfiguration zu `claude_desktop_config.json` hinzu:

```json
{
  "mcpServers": {
    "prestashop": {
      "command": "python",
      "args": ["-m", "prestashop_mcp.prestashop_mcp_server"],
      "cwd": "/path/to/prestashop-mcp",
      "env": {
        "PRESTASHOP_SHOP_URL": "https://ihr-shop.example.com",
        "PRESTASHOP_API_KEY": "IHR_API_KEY"
      }
    }
  }
}
```

### 💻 CLI Verwendung

```bash
# Mit Environment Variablen
prestashop-mcp

# Mit direkten Parametern
prestashop-mcp --shop-url https://ihr-shop.com --api-key IHR_API_KEY

# Debug Modus
prestashop-mcp --log-level DEBUG
```

### 🧪 Testing

```bash
# Vollständige CRUD-Tests ausführen
python test_crud_operations.py

# Unit Tests
pytest

# Tests mit Coverage
pytest --cov=src/prestashop_mcp --cov-report=html
```

## 📊 Projektstruktur

```
prestashop-mcp/
├── src/prestashop_mcp/                  # Main Package
│   ├── prestashop_mcp_server.py         # MCP Server
│   ├── prestashop_client.py             # PrestaShop API Client
│   ├── config.py                        # Configuration Management
│   └── cli.py                          # Command Line Interface
├── test_crud_operations.py              # CRUD Test Suite
├── tests/                               # Unit Tests
├── README.md                            # Documentation
├── pyproject.toml                       # Package Configuration
└── requirements.txt                     # Dependencies
```

## 📖 API Dokumentation

### PrestaShop API

Die vollständige PrestaShop API Dokumentation:
- **[PrestaShop DevDocs - Webservice](https://devdocs.prestashop-project.org/8/webservice/)**

### Authentifizierung

```bash
curl -u "API_KEY:" https://ihr-shop.com/api/configurations?output_format=JSON
```

### Wichtige Endpoints

- **Produkte**: `/api/products`
- **Kategorien**: `/api/categories`
- **Kunden**: `/api/customers`
- **Bestellungen**: `/api/orders`
- **Lagerbestände**: `/api/stock_availables`
- **Bestellstatus**: `/api/order_states`

## 🧪 Entwicklung

### 🏗️ Entwicklungsumgebung

```bash
# Development Dependencies
pip install -r requirements.txt
pip install -r tests/requirements.txt

# Tests ausführen
pytest

# Tests mit Coverage
pytest --cov=src/prestashop_mcp --cov-report=html
```

## 📖 Ressourcen

- **[PrestaShop Official Documentation](https://devdocs.prestashop-project.org/)**
- **[Model Context Protocol Specification](https://modelcontextprotocol.io/)**
- **[Claude Desktop MCP Integration](https://docs.anthropic.com/)**
- **[GitHub Repository](https://github.com/latinogino/prestashop-mcp)**

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

## 📝 Changelog

### v1.0.0 - Production Release
- ✨ Vollständige Shop-Verwaltung mit professionellen Tools
- 📦 Erweiterte Produkt-Features (Lager, Preise, Referenzen)
- 🏷️ Kategorie-Management mit Hierarchie-Support
- 👥 Kunden-Verwaltung (Erstellen, Bearbeiten)
- 📋 Bestell-Management mit Status-Updates
- ⚙️ Shop-Statistiken und Konfiguration
- 🛡️ Production-Ready mit umfassenden Tests
- 📖 Vollständige Dokumentation mit Praxis-Beispielen

---

**🎯 Verwalten Sie Ihren kompletten PrestaShop über natürliche Sprache mit Claude Desktop!**