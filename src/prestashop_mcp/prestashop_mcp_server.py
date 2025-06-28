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

# Import our PrestaShop components
from .config import Config
from .prestashop_client import PrestaShopClient, PrestaShopAPIError


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


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    """Handle all tool calls using the PrestaShopClient with proper XML support."""
    
    try:
        # Initialize the config and client
        config = Config()
        
        async with PrestaShopClient(config) as client:
            
            # Connection & Info
            if name == "test_connection":
                result = await client.get_configurations()
                if 'error' not in result:
                    result = {"status": "success", "message": "API connection working", "xml_enabled": True}
            
            elif name == "get_shop_info":
                result = await client.get_shop_info()
            
            # Categories CRUD
            elif name == "get_categories":
                result = await client.get_categories(
                    limit=arguments.get('limit', 10),
                    parent_id=arguments.get('parent_id')
                )
            
            elif name == "create_category":
                result = await client.create_category(
                    name=arguments['name'],
                    description=arguments.get('description'),
                    parent_id=arguments.get('parent_id', '2'),
                    active=arguments.get('active', True)
                )
            
            elif name == "update_category":
                result = await client.update_category(
                    category_id=arguments['category_id'],
                    name=arguments.get('name'),
                    description=arguments.get('description'),
                    active=arguments.get('active')
                )
            
            elif name == "delete_category":
                result = await client.delete_category(arguments['category_id'])
            
            # Unified Products Management
            elif name == "get_products":
                # Build filters dictionary
                filters = {}
                if arguments.get('category_id'):
                    filters['category'] = arguments['category_id']
                if arguments.get('name_filter'):
                    filters['name'] = arguments['name_filter']
                
                result = await client.get_products(
                    product_id=arguments.get('product_id'),
                    limit=arguments.get('limit', 10),
                    filters=filters if filters else None,
                    include_details=arguments.get('include_details', False),
                    include_stock=arguments.get('include_stock', False),
                    include_category_info=arguments.get('include_category_info', False),
                    display=arguments.get('display')
                )
            
            elif name == "create_product":
                result = await client.create_product(
                    name=arguments['name'],
                    price=arguments['price'],
                    description=arguments.get('description'),
                    category_id=arguments.get('category_id'),
                    quantity=arguments.get('quantity'),
                    reference=arguments.get('reference'),
                    weight=arguments.get('weight')
                )
            
            elif name == "update_product":
                # Prepare kwargs for update
                update_kwargs = {}
                for key in ['name', 'price', 'description', 'category_id', 'active']:
                    if key in arguments:
                        update_kwargs[key] = arguments[key]
                
                result = await client.update_product(
                    product_id=arguments['product_id'],
                    **update_kwargs
                )
            
            elif name == "delete_product":
                result = await client.delete_product(arguments['product_id'])
            
            elif name == "update_product_stock":
                result = await client.update_product_stock(
                    product_id=arguments['product_id'],
                    quantity=arguments['quantity']
                )
            
            elif name == "update_product_price":
                result = await client.update_product_price(
                    product_id=arguments['product_id'],
                    price=arguments['price'],
                    wholesale_price=arguments.get('wholesale_price')
                )
            
            # Customers CRUD
            elif name == "get_customers":
                result = await client.get_customers(
                    limit=arguments.get('limit', 10),
                    email=arguments.get('email_filter')
                )
            
            elif name == "create_customer":
                result = await client.create_customer(
                    email=arguments['email'],
                    firstname=arguments['firstname'],
                    lastname=arguments['lastname'],
                    password=arguments['password'],
                    active=arguments.get('active', True)
                )
            
            elif name == "update_customer":
                # Prepare kwargs for update
                update_kwargs = {}
                for key in ['email', 'firstname', 'lastname', 'active']:
                    if key in arguments:
                        update_kwargs[key] = arguments[key]
                
                result = await client.update_customer(
                    customer_id=arguments['customer_id'],
                    **update_kwargs
                )
            
            # Orders
            elif name == "get_orders":
                result = await client.get_orders(
                    limit=arguments.get('limit', 10),
                    customer_id=arguments.get('customer_id'),
                    status=arguments.get('status')
                )
            
            elif name == "update_order_status":
                result = await client.update_order_status(
                    order_id=arguments['order_id'],
                    status_id=arguments['status_id']
                )
            
            elif name == "get_order_states":
                result = await client.get_order_states()
            
            else:
                result = {"error": f"Unknown tool: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    except PrestaShopAPIError as e:
        error_result = {"error": f"PrestaShop API Error: {str(e)}", "type": "api_error"}
        return [TextContent(type="text", text=json.dumps(error_result, indent=2))]
    
    except Exception as e:
        error_result = {"error": f"Tool execution failed: {str(e)}", "type": "internal_error"}
        return [TextContent(type="text", text=json.dumps(error_result, indent=2))]


async def main():
    """Run the PrestaShop MCP server."""
    # Quick API test using the proper client
    try:
        config = Config()
        async with PrestaShopClient(config) as client:
            print("🧪 Testing API connection with XML support...", file=sys.stderr)
            result = await client.get_configurations()
            if 'error' not in result:
                print("✅ API connection successful with XML support", file=sys.stderr)
            else:
                print(f"❌ API test failed: {result.get('error')}", file=sys.stderr)
                return
    except Exception as e:
        print(f"❌ API test error: {e}", file=sys.stderr)
        return
    
    # Run server
    print("🚀 Starting PrestaShop MCP server with proper XML integration...", file=sys.stderr)
    print("✅ Server ready with unified product API, XML support, and full CRUD operations", file=sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="prestashop-mcp",
                server_version="2.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
