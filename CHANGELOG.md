# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2025-06-30 - Extended Functionality (LATEST)

### Added
- ✨ **NEW**: Module Management - Install, activate, deactivate modules
- ✨ **NEW**: ps_mainmenu Management - Complete navigation control
- ✨ **NEW**: Cache Management - Clear cache and monitor status
- ✨ **NEW**: Theme Management - Configure theme settings
- 🔧 **Enhanced**: Comprehensive store administration tools
- 📊 **Extended**: 12 new MCP tools for advanced functionality
- 🏗️ **Professional**: Enterprise-level PrestaShop management

### New Tools
- `get_modules` - List all PrestaShop modules
- `get_module_by_name` - Get specific module details
- `install_module` - Install new modules
- `update_module_status` - Activate/deactivate modules
- `get_main_menu_links` - Retrieve ps_mainmenu navigation links
- `update_main_menu_link` - Edit existing menu links
- `add_main_menu_link` - Add new navigation links
- `clear_cache` - Clear PrestaShop cache (all types)
- `get_cache_status` - Monitor cache configuration
- `get_themes` - Get current theme information
- `update_theme_setting` - Configure theme settings

## [2.0.0] - 2025-06-28 - Unified Product API (BREAKING CHANGES)

### Added
- ✨ **MAJOR**: Unified `get_products` API handles all product retrieval scenarios
- 🔧 **Enhanced**: Single API call for both individual products and lists
- 📊 **Flexible**: Optional enhancement with stock, category, and custom field selection
- 🏗️ **Cleaner**: Eliminates API duplication and provides intuitive interface

### Removed
- 🗑️ **REMOVED**: `get_product_details` method (functionality merged into `get_products`)

### Breaking Changes
- Update your integrations to use the new unified `get_products` method instead of `get_product_details`

## [1.1.0] - 2025-06-27 - Enhanced Product Details

### Added
- ✨ **NEW**: `get_product_details` method for comprehensive product information
- 📊 Enhanced product queries with stock and category information
- 🔍 Flexible field selection with display parameter
- 🏗️ Improved API client architecture for detailed data retrieval

## [1.0.0] - 2025-06-27 - Production Release

### Added
- ✨ Complete store management with professional tools
- 📦 Enhanced product features (inventory, prices, references)
- 🏷️ Category management with hierarchy support
- 👥 Customer management (create, edit)
- 📋 Order management with status updates
- ⚙️ Store statistics and configuration
- 🛡️ Production-ready with comprehensive tests
- 📖 Complete documentation with practical examples

### Features
- **Products**: Full CRUD operations with unified API
- **Categories**: Complete hierarchy management
- **Customers**: Customer lifecycle management
- **Orders**: Status tracking and management
- **Store Admin**: Statistics and configuration access
- **Testing**: Comprehensive test suite
- **Documentation**: Complete setup and usage guides

## [0.1.0] - 2025-06-26 - Initial Development

### Added
- Initial project structure
- Basic PrestaShop API integration
- MCP server foundation
- Core product management functionality
