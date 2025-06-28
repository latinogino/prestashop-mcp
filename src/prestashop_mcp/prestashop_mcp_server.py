"""Professional PrestaShop MCP Server with comprehensive CRUD operations."""

import asyncio
import json
import sys
import os

# Import MCP components
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import aiohttp
from aiohttp import BasicAuth


# Create server instance
server = Server("prestashop-mcp")


@server.list_tools()
async def handle_list_tools():
    """List all available tools."""
    return [
        # Connection & Info
        Tool(
            name="test_connection",
            description="Test PrestaShop API connection",
            inputSchema={"type": "object", "properties": {}, "additionalProperties": False}
        ),
        Tool(
            name="get_shop_info",
            description="Get general shop information and statistics",
            inputSchema={"type": "object", "properties": {}, "additionalProperties": False}
        ),
        
        # Categories CRUD
        Tool(
            name="get_categories",
            description="Get PrestaShop categories",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of categories to retrieve", "default": 10},
                    "parent_id": {"type": "string", "description": "Filter by parent category ID"}
                },
                "additionalProperties": False
            }
        ),
        Tool(
            name="create_category",
            description="Create a new category",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Category name"},
                    "description": {"type": "string", "description": "Category description"},
                    "parent_id": {"type": "string", "description": "Parent category ID", "default": "2"},
                    "active": {"type": "boolean", "description": "Whether category is active", "default": True}
                },
                "required": ["name"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="update_category",
            description="Update an existing category",
            inputSchema={
                "type": "object",
                "properties": {
                    "category_id": {"type": "string", "description": "Category ID to update"},
                    "name": {"type": "string", "description": "New category name"},
                    "description": {"type": "string", "description": "New category description"},
                    "active": {"type": "boolean", "description": "Whether category is active"}
                },
                "required": ["category_id"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="delete_category",
            description="Delete a category",
            inputSchema={
                "type": "object",
                "properties": {
                    "category_id": {"type": "string", "description": "Category ID to delete"}
                },
                "required": ["category_id"],
                "additionalProperties": False
            }
        ),
        
        # Unified Products Management
        Tool(
            name="get_products",
            description="Unified product retrieval - supports both single product by ID and multiple products with comprehensive filtering and enhancement options",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "Retrieve single product by ID (takes precedence over other params)"},
                    "limit": {"type": "integer", "description": "Number of products to retrieve for list queries", "default": 10},
                    "category_id": {"type": "string", "description": "Filter by category ID"},
                    "name_filter": {"type": "string", "description": "Filter by product name"},
                    "include_details": {"type": "boolean", "description": "Include complete product information", "default": False},
                    "include_stock": {"type": "boolean", "description": "Include stock/inventory information", "default": False},
                    "include_category_info": {"type": "boolean", "description": "Include category details", "default": False},
                    "display": {"type": "string", "description": "Comma-separated list of specific fields to include (e.g., 'id,name,price')"}
                },
                "additionalProperties": False
            }
        ),
        Tool(
            name="create_product",
            description="Create a new product",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Product name"},
                    "price": {"type": "number", "description": "Product price"},
                    "description": {"type": "string", "description": "Product description"},
                    "category_id": {"type": "string", "description": "Category ID"},
                    "quantity": {"type": "integer", "description": "Initial stock quantity"},
                    "reference": {"type": "string", "description": "Product reference/SKU"},
                    "weight": {"type": "number", "description": "Product weight"}
                },
                "required": ["name", "price"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="update_product",
            description="Update an existing product",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "Product ID to update"},
                    "name": {"type": "string", "description": "New product name"},
                    "price": {"type": "number", "description": "New product price"},
                    "description": {"type": "string", "description": "New product description"},
                    "category_id": {"type": "string", "description": "New category ID"},
                    "active": {"type": "boolean", "description": "Whether product is active"}
                },
                "required": ["product_id"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="delete_product",
            description="Delete a product",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "Product ID to delete"}
                },
                "required": ["product_id"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="update_product_stock",
            description="Update product stock quantity",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "Product ID"},
                    "quantity": {"type": "integer", "description": "New stock quantity"}
                },
                "required": ["product_id", "quantity"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="update_product_price",
            description="Update product price",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "Product ID"},
                    "price": {"type": "number", "description": "New price"},
                    "wholesale_price": {"type": "number", "description": "New wholesale price"}
                },
                "required": ["product_id", "price"],
                "additionalProperties": False
            }
        ),
        
        # Customers CRUD
        Tool(
            name="get_customers",
            description="Get PrestaShop customers",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of customers to retrieve", "default": 10},
                    "email_filter": {"type": "string", "description": "Filter by email"}
                },
                "additionalProperties": False
            }
        ),
        Tool(
            name="create_customer",
            description="Create a new customer",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Customer email"},
                    "firstname": {"type": "string", "description": "First name"},
                    "lastname": {"type": "string", "description": "Last name"},
                    "password": {"type": "string", "description": "Customer password"},
                    "active": {"type": "boolean", "description": "Whether customer is active", "default": True}
                },
                "required": ["email", "firstname", "lastname", "password"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="update_customer",
            description="Update an existing customer",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "Customer ID to update"},
                    "email": {"type": "string", "description": "New email"},
                    "firstname": {"type": "string", "description": "New first name"},
                    "lastname": {"type": "string", "description": "New last name"},
                    "active": {"type": "boolean", "description": "Whether customer is active"}
                },
                "required": ["customer_id"],
                "additionalProperties": False
            }
        ),
        
        # Orders
        Tool(
            name="get_orders",
            description="Get PrestaShop orders",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of orders to retrieve", "default": 10},
                    "customer_id": {"type": "string", "description": "Filter by customer ID"},
                    "status": {"type": "string", "description": "Filter by order status"}
                },
                "additionalProperties": False
            }
        ),
        Tool(
            name="update_order_status",
            description="Update order status",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "Order ID"},
                    "status_id": {"type": "string", "description": "New status ID"}
                },
                "required": ["order_id", "status_id"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="get_order_states",
            description="Get available order states/statuses",
            inputSchema={"type": "object", "properties": {}, "additionalProperties": False}
        )
    ]


async def make_api_request(method: str, endpoint: str, params=None, data=None):
    """Make HTTP request to PrestaShop API."""
    api_key = os.getenv('PRESTASHOP_API_KEY')
    shop_url = os.getenv('PRESTASHOP_SHOP_URL')
    
    if not api_key or not shop_url:
        return {"error": "Missing API credentials"}
    
    if params is None:
        params = {}
    params['output_format'] = 'JSON'
    
    url = f"{shop_url.rstrip('/')}/api/{endpoint}"
    
    try:
        async with aiohttp.ClientSession() as session:
            auth = BasicAuth(api_key, '')
            headers = {}
            if data:
                headers['Content-Type'] = 'application/json'
            
            async with session.request(
                method=method,
                url=url,
                auth=auth,
                params=params,
                json=data,
                headers=headers
            ) as response:
                if response.status >= 400:
                    error_text = await response.text()
                    return {"error": f"API request failed with status {response.status}: {error_text}"}
                
                response_text = await response.text()
                if not response_text:
                    return {}
                
                try:
                    return json.loads(response_text)
                except json.JSONDecodeError:
                    return {"raw_response": response_text}
    
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


def generate_link_rewrite(name: str) -> str:
    """Generate URL-friendly link rewrite from name."""
    import re
    link_rewrite = re.sub(r'[^a-zA-Z0-9\s]', '', name.lower())
    link_rewrite = re.sub(r'\s+', '-', link_rewrite.strip())
    return link_rewrite


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    """Handle all tool calls."""
    
    try:
        # Connection & Info
        if name == "test_connection":
            result = await make_api_request('GET', 'configurations', {'limit': 1})
            if 'error' not in result:
                result = {"status": "success", "message": "API connection working"}
        
        elif name == "get_shop_info":
            configs = await make_api_request('GET', 'configurations', {'limit': 1})
            if 'configurations' in configs:
                result = {
                    "status": "success",
                    "shop_info": {
                        "api_working": True,
                        "configurations_count": len(configs.get('configurations', []))
                    }
                }
            else:
                result = {"error": "Could not retrieve shop info"}
        
        # Categories CRUD
        elif name == "get_categories":
            params = {'limit': arguments.get('limit', 10)}
            if arguments.get('parent_id'):
                params['filter[id_parent]'] = arguments['parent_id']
            result = await make_api_request('GET', 'categories', params)
        
        elif name == "create_category":
            category_data = {
                "category": {
                    "name": {"language": [{"id": "1", "value": arguments['name']}]},
                    "link_rewrite": {"language": [{"id": "1", "value": generate_link_rewrite(arguments['name'])}]},
                    "id_parent": arguments.get('parent_id', '2'),
                    "active": "1" if arguments.get('active', True) else "0"
                }
            }
            if arguments.get('description'):
                category_data["category"]["description"] = {
                    "language": [{"id": "1", "value": arguments['description']}]
                }
            result = await make_api_request('POST', 'categories', data=category_data)
        
        elif name == "update_category":
            # Get existing category first
            existing = await make_api_request('GET', f"categories/{arguments['category_id']}")
            if 'category' not in existing:
                result = {"error": f"Category {arguments['category_id']} not found"}
            else:
                category_data = existing['category']
                
                if 'name' in arguments:
                    category_data['name'] = {"language": [{"id": "1", "value": arguments['name']}]}
                    category_data['link_rewrite'] = {
                        "language": [{"id": "1", "value": generate_link_rewrite(arguments['name'])}]
                    }
                if 'description' in arguments:
                    category_data['description'] = {
                        "language": [{"id": "1", "value": arguments['description']}]
                    }
                if 'active' in arguments:
                    category_data['active'] = "1" if arguments['active'] else "0"
                
                result = await make_api_request('PUT', f"categories/{arguments['category_id']}", 
                                              data={"category": category_data})
        
        elif name == "delete_category":
            result = await make_api_request('DELETE', f"categories/{arguments['category_id']}")
        
        # Unified Products Management
        elif name == "get_products":
            # Build filters dictionary
            filters = {}
            if arguments.get('category_id'):
                filters['category'] = arguments['category_id']
            if arguments.get('name_filter'):
                filters['name'] = arguments['name_filter']
            
            # Build parameters for the unified API call
            api_params = {
                'product_id': arguments.get('product_id'),
                'limit': arguments.get('limit', 10),
                'filters': filters if filters else None,
                'include_details': arguments.get('include_details', False),
                'include_stock': arguments.get('include_stock', False),
                'include_category_info': arguments.get('include_category_info', False),
                'display': arguments.get('display')
            }
            
            # Remove None values
            api_params = {k: v for k, v in api_params.items() if v is not None}
            
            # Use the unified client method (we'll simulate this for now since we don't have direct access)
            if arguments.get('product_id'):
                # Single product by ID
                product_id = arguments['product_id']
                params = {}
                if arguments.get('display'):
                    params['display'] = arguments['display']
                
                # Get main product data
                product_data = await make_api_request('GET', f'products/{product_id}', params)
                
                if 'product' not in product_data:
                    result = {"error": f"Product {product_id} not found"}
                else:
                    result = product_data.copy()
                    
                    # Add enhanced information if requested
                    if arguments.get('include_stock', False):
                        try:
                            stock_params = {'filter[id_product]': product_id}
                            stock_response = await make_api_request('GET', 'stock_availables', stock_params)
                            
                            if 'stock_availables' in stock_response and stock_response['stock_availables']:
                                result['stock_info'] = stock_response['stock_availables'][0]
                            else:
                                result['stock_info'] = {"error": "Stock information not available"}
                        except Exception as e:
                            result['stock_info'] = {"error": f"Stock retrieval failed: {str(e)}"}
                    
                    if arguments.get('include_category_info', False):
                        try:
                            category_id = product_data['product'].get('id_category_default')
                            if category_id:
                                category_response = await make_api_request('GET', f'categories/{category_id}')
                                if 'category' in category_response:
                                    result['category_info'] = category_response['category']
                                else:
                                    result['category_info'] = {"error": "Category not found"}
                            else:
                                result['category_info'] = {"error": "No default category assigned"}
                        except Exception as e:
                            result['category_info'] = {"error": f"Category retrieval failed: {str(e)}"}
            else:
                # Multiple products
                params = {'limit': arguments.get('limit', 10)}
                if arguments.get('display'):
                    params['display'] = arguments['display']
                if arguments.get('category_id'):
                    params['filter[id_category_default]'] = arguments['category_id']
                if arguments.get('name_filter'):
                    params['filter[name]'] = f"[{arguments['name_filter']}]%"
                
                result = await make_api_request('GET', 'products', params)
                
                # Add enhanced information if requested and we have products
                if (arguments.get('include_details') or arguments.get('include_stock') or arguments.get('include_category_info')) and 'products' in result:
                    enhanced_products = []
                    
                    for product in result['products']:
                        product_id = product.get('id')
                        if product_id:
                            try:
                                # Get detailed product info
                                detail_params = {}
                                if arguments.get('display'):
                                    detail_params['display'] = arguments['display']
                                
                                detailed_product = await make_api_request('GET', f'products/{product_id}', detail_params)
                                
                                if 'product' in detailed_product:
                                    enhanced_product = detailed_product.copy()
                                    
                                    # Add stock info if requested
                                    if arguments.get('include_stock', False):
                                        try:
                                            stock_params = {'filter[id_product]': product_id}
                                            stock_response = await make_api_request('GET', 'stock_availables', stock_params)
                                            if 'stock_availables' in stock_response and stock_response['stock_availables']:
                                                enhanced_product['stock_info'] = stock_response['stock_availables'][0]
                                        except Exception:
                                            enhanced_product['stock_info'] = {"error": "Stock retrieval failed"}
                                    
                                    # Add category info if requested
                                    if arguments.get('include_category_info', False):
                                        try:
                                            category_id = detailed_product['product'].get('id_category_default')
                                            if category_id:
                                                category_response = await make_api_request('GET', f'categories/{category_id}')
                                                if 'category' in category_response:
                                                    enhanced_product['category_info'] = category_response['category']
                                        except Exception:
                                            enhanced_product['category_info'] = {"error": "Category retrieval failed"}
                                    
                                    enhanced_products.append(enhanced_product)
                                else:
                                    enhanced_products.append(product)
                            except Exception as e:
                                enhanced_products.append(product)
                        else:
                            enhanced_products.append(product)
                    
                    result['products'] = enhanced_products
        
        elif name == "create_product":
            product_data = {
                "product": {
                    "name": {"language": [{"id": "1", "value": arguments['name']}]},
                    "price": str(arguments['price']),
                    "active": "1",
                    "state": "1",
                    "available_for_order": "1",
                    "show_price": "1",
                    "link_rewrite": {"language": [{"id": "1", "value": generate_link_rewrite(arguments['name'])}]}
                }
            }
            
            if arguments.get('description'):
                product_data["product"]["description"] = {
                    "language": [{"id": "1", "value": arguments['description']}]
                }
                product_data["product"]["description_short"] = {
                    "language": [{"id": "1", "value": arguments['description'][:400]}]
                }
            
            if arguments.get('reference'):
                product_data["product"]["reference"] = arguments['reference']
            
            if arguments.get('weight'):
                product_data["product"]["weight"] = str(arguments['weight'])
            
            if arguments.get('category_id'):
                product_data["product"]["id_category_default"] = arguments['category_id']
            
            result = await make_api_request('POST', 'products', data=product_data)
            
            # Update stock if quantity specified
            if arguments.get('quantity') and 'product' in result and 'id' in result['product']:
                product_id = result['product']['id']
                stock_result = await update_stock_quantity(product_id, arguments['quantity'])
                result['stock_update'] = stock_result
        
        elif name == "update_product":
            # Get existing product first
            existing = await make_api_request('GET', f"products/{arguments['product_id']}")
            if 'product' not in existing:
                result = {"error": f"Product {arguments['product_id']} not found"}
            else:
                product_data = existing['product']
                
                if 'name' in arguments:
                    product_data['name'] = {"language": [{"id": "1", "value": arguments['name']}]}
                    product_data['link_rewrite'] = {
                        "language": [{"id": "1", "value": generate_link_rewrite(arguments['name'])}]
                    }
                if 'price' in arguments:
                    product_data['price'] = str(arguments['price'])
                if 'description' in arguments:
                    product_data['description'] = {
                        "language": [{"id": "1", "value": arguments['description']}]
                    }
                if 'category_id' in arguments:
                    product_data['id_category_default'] = arguments['category_id']
                if 'active' in arguments:
                    product_data['active'] = "1" if arguments['active'] else "0"
                
                result = await make_api_request('PUT', f"products/{arguments['product_id']}", 
                                              data={"product": product_data})
        
        elif name == "delete_product":
            result = await make_api_request('DELETE', f"products/{arguments['product_id']}")
        
        elif name == "update_product_stock":
            result = await update_stock_quantity(arguments['product_id'], arguments['quantity'])
        
        elif name == "update_product_price":
            # Get existing product first
            existing = await make_api_request('GET', f"products/{arguments['product_id']}")
            if 'product' not in existing:
                result = {"error": f"Product {arguments['product_id']} not found"}
            else:
                product_data = existing['product']
                product_data['price'] = str(arguments['price'])
                if arguments.get('wholesale_price'):
                    product_data['wholesale_price'] = str(arguments['wholesale_price'])
                
                result = await make_api_request('PUT', f"products/{arguments['product_id']}", 
                                              data={"product": product_data})
        
        # Customers CRUD
        elif name == "get_customers":
            params = {'limit': arguments.get('limit', 10)}
            if arguments.get('email_filter'):
                params['filter[email]'] = f"[{arguments['email_filter']}]%"
            result = await make_api_request('GET', 'customers', params)
        
        elif name == "create_customer":
            customer_data = {
                "customer": {
                    "email": arguments['email'],
                    "firstname": arguments['firstname'],
                    "lastname": arguments['lastname'],
                    "passwd": arguments['password'],
                    "active": "1" if arguments.get('active', True) else "0",
                    "id_default_group": "3"
                }
            }
            result = await make_api_request('POST', 'customers', data=customer_data)
        
        elif name == "update_customer":
            # Get existing customer first
            existing = await make_api_request('GET', f"customers/{arguments['customer_id']}")
            if 'customer' not in existing:
                result = {"error": f"Customer {arguments['customer_id']} not found"}
            else:
                customer_data = existing['customer']
                
                if 'email' in arguments:
                    customer_data['email'] = arguments['email']
                if 'firstname' in arguments:
                    customer_data['firstname'] = arguments['firstname']
                if 'lastname' in arguments:
                    customer_data['lastname'] = arguments['lastname']
                if 'active' in arguments:
                    customer_data['active'] = "1" if arguments['active'] else "0"
                
                result = await make_api_request('PUT', f"customers/{arguments['customer_id']}", 
                                              data={"customer": customer_data})
        
        # Orders
        elif name == "get_orders":
            params = {'limit': arguments.get('limit', 10)}
            if arguments.get('customer_id'):
                params['filter[id_customer]'] = arguments['customer_id']
            if arguments.get('status'):
                params['filter[current_state]'] = arguments['status']
            result = await make_api_request('GET', 'orders', params)
        
        elif name == "update_order_status":
            history_data = {
                "order_history": {
                    "id_order": arguments['order_id'],
                    "id_order_state": arguments['status_id'],
                    "id_employee": "1"
                }
            }
            result = await make_api_request('POST', 'order_histories', data=history_data)
        
        elif name == "get_order_states":
            result = await make_api_request('GET', 'order_states')
        
        else:
            result = {"error": f"Unknown tool: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": f"Tool execution failed: {str(e)}"}, indent=2))]


async def update_stock_quantity(product_id: str, quantity: int):
    """Helper function to update product stock."""
    # Get stock availables for this product
    stock_params = {'filter[id_product]': product_id}
    stock_response = await make_api_request('GET', 'stock_availables', stock_params)
    
    if 'stock_availables' in stock_response and stock_response['stock_availables']:
        stock_id = stock_response['stock_availables'][0]['id']
        
        stock_data = {
            "stock_available": {
                "id": stock_id,
                "id_product": product_id,
                "quantity": str(quantity)
            }
        }
        
        return await make_api_request('PUT', f'stock_availables/{stock_id}', data=stock_data)
    else:
        return {"error": f"Stock information not found for product {product_id}"}


async def main():
    """Run the PrestaShop MCP server."""
    # Quick API test
    api_key = os.getenv('PRESTASHOP_API_KEY')
    shop_url = os.getenv('PRESTASHOP_SHOP_URL')
    
    if not api_key or not shop_url:
        print("❌ Missing environment variables", file=sys.stderr)
        return
    
    print("🧪 Testing API connection...", file=sys.stderr)
    try:
        async with aiohttp.ClientSession() as session:
            auth = BasicAuth(api_key, '')
            url = f"{shop_url.rstrip('/')}/api/configurations"
            params = {'output_format': 'JSON', 'limit': 1}
            
            async with session.get(url, auth=auth, params=params) as response:
                if response.status == 200:
                    print("✅ API connection successful", file=sys.stderr)
                else:
                    print(f"❌ API test failed: {response.status}", file=sys.stderr)
                    return
    except Exception as e:
        print(f"❌ API test error: {e}", file=sys.stderr)
        return
    
    # Run server
    print("🚀 Starting PrestaShop MCP server...", file=sys.stderr)
    print("✅ Server ready with unified product API and full CRUD operations", file=sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="prestashop-mcp",
                server_version="2.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())