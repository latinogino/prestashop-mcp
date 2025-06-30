# PrestaShop MCP Testing Guide

## Testing After Code Updates

### Prerequisites
- Python 3.8+ installed
- PrestaShop instance with API access
- Valid PrestaShop API key and URL

## Setup Test Environment

### Windows
```cmd
# Navigate to project directory
cd prestashop-mcp

# Activate virtual environment
.\venv_prestashop\Scripts\Activate.ps1

# Update code from repository
git pull origin main

# Install/update the package
pip install -e .

# Install test dependencies
cd tests
pip install -r requirements.txt

# Update code from repository
git pull origin main

# Install/update the package
pip install -e .

# Install test dependencies
cd tests
pip install -r requirements.txt
```

### macOS/Linux
```bash
# Navigate to project directory
cd prestashop-mcp

# Update code from repository
git pull origin main

# Install/update the package
pip install -e .

# Install test dependencies
cd tests
pip install -r requirements.txt
```

### Configuration

1. Set up your PrestaShop API credentials as environment variables:

**Windows (PowerShell):**
```powershell
$env:PRESTASHOP_API_URL="https://your-shop.domain/api"
$env:PRESTASHOP_API_KEY="your_api_key_here"
```

**macOS/Linux (Bash):**
```bash
export PRESTASHOP_API_URL="https://your-shop.domain/api"
export PRESTASHOP_API_KEY="your_api_key_here"
```

## Running Test Scripts

### Test Script Overview

- **`test_crud_operations.py`** - Comprehensive CRUD testing (Create, Read, Update, Delete)
- **`test_config.py`** - Configuration and connection testing

### Running Individual Test Scripts

**Comprehensive CRUD Test:**
```bash
# Run complete CRUD test suite
python test_crud_operations.py
```

**Configuration Test:**
```bash
# Test API configuration and connection
python test_config.py
```

### Using pytest (Optional)

```bash
# Run all tests with pytest
pytest

# Run with coverage report
pytest --cov=../src/prestashop_mcp

# Run specific test file
pytest test_crud_operations.py

# Verbose output
pytest -v
```

## Test Results

### What the Tests Verify

**Connection Tests:**
- API authentication
- Shop info retrieval
- Basic connectivity

**CRUD Operations:**
- ✅ Category creation, update, deletion
- ✅ Product creation with correct `state=1` (Backend visibility)
- ✅ Product updates (name, price, stock)
- ✅ Customer creation and updates
- ✅ Order status operations

### Expected Output

**Successful test run:**
```
🚀 Starting Comprehensive CRUD Test Suite
============================================================
✅ PASS: READ Categories
✅ PASS: READ Products
✅ PASS: Category CREATE
✅ PASS: Category UPDATE
✅ PASS: Category DELETE
✅ PASS: Product CREATE
✅ PASS: Product UPDATE
✅ PASS: Product STOCK UPDATE
✅ PASS: Product PRICE UPDATE
✅ PASS: Product DELETE

📊 TEST SUMMARY
============================================================
Total Tests: 15
✅ Passed: 15
❌ Failed: 0
Success Rate: 100.0%

🎉 PERFECT! All CRUD operations working correctly!
```

## Restart Requirement

**Important:** After updating the MCP server code, you must restart Claude Desktop completely for the changes to take effect. This is due to client-side caching of tool definitions.

## Manual Testing in Claude Desktop

After running the test scripts successfully, verify in Claude Desktop:

1. **Test connection:**
   ```
   Use prestashop:test_connection
   ```

2. **Create a test product:**
   ```
   Create a test product "Test Product 2025" for €25.99 in category 2
   ```

3. **Verify backend visibility:**
   - Check your PrestaShop admin panel
   - The product should appear immediately in the product list
   - It should have `state=1` (published status)

## Troubleshooting

**Common Issues:**

1. **Import errors:**
   ```bash
   # Reinstall the package
   pip install -e ../
   ```

2. **API connection fails:**
   ```bash
   # Test configuration
   python test_config.py
   ```

3. **Old behavior persists:**
   - Restart Claude Desktop completely
   - Verify environment variables are set
   - Check API key permissions in PrestaShop

4. **XML parsing errors (should be fixed):**
   - If you still see XML errors, ensure you pulled the latest code
   - Run `pip install -e .` again

## Development

**For contributors making changes:**

```bash
# Run tests before committing
python test_crud_operations.py

# Check specific functionality
python test_config.py

# Run with pytest for detailed output
pytest -v --tb=short
```

## Test Data Cleanup

The test scripts automatically clean up test data (categories, products, customers) after each test run. If tests are interrupted, you may need to manually remove test entries from your PrestaShop admin panel.

Test entries are prefixed with:
- Categories: "Test Category CRUD [timestamp]"
- Products: "Test Product CRUD [timestamp]"
- Customers: "test-crud-[timestamp]@example.com"
