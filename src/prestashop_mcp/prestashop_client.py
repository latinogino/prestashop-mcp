"""PrestaShop API Client with CORRECT XML Structure per Official Documentation."""

import asyncio
import json
import logging
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import aiohttp
from aiohttp import BasicAuth

from .config import Config


class PrestaShopAPIError(Exception):
    """PrestaShop API Error."""
    pass


class PrestaShopClient:
    """PrestaShop API Client with CORRECT XML structure per official documentation."""
    
    def __init__(self, config: Config):
        self.config = config
        self.base_url = config.shop_url.rstrip('/') + '/api/'
        self.auth = BasicAuth(config.api_key, '')
        self.session: Optional[aiohttp.ClientSession] = None
        self.available_languages = [
            {"id": 1, "name": "Default"},
            {"id": 2, "name": "Secondary"}
        ]  # Default language setup - can be enhanced with dynamic detection
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                auth=self.auth,
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self.session
    
    def _dict_to_xml(self, data: Dict[str, Any], root_name: str = "prestashop") -> str:
        """Convert dictionary to XML format with CORRECT PrestaShop multilingual structure."""
        def build_element(parent: ET.Element, key: str, value: Any):
            if isinstance(value, list) and value and isinstance(value[0], dict) and "id" in value[0] and "value" in value[0]:
                # This is a multilingual field - create nested structure
                # <name><language id="1">value</language><language id="2">value</language></name>
                container = ET.SubElement(parent, key)
                for lang_item in value:
                    language_elem = ET.SubElement(container, "language")
                    language_elem.set("id", str(lang_item["id"]))
                    language_elem.text = str(lang_item["value"]) if lang_item["value"] is not None else ""
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        element = ET.SubElement(parent, key)
                        for sub_key, sub_value in item.items():
                            build_element(element, sub_key, sub_value)
                    else:
                        element = ET.SubElement(parent, key)
                        element.text = str(item) if item is not None else ""
            elif isinstance(value, dict):
                element = ET.SubElement(parent, key)
                for sub_key, sub_value in value.items():
                    build_element(element, sub_key, sub_value)
            else:
                element = ET.SubElement(parent, key)
                element.text = str(value) if value is not None else ""
        
        # Always wrap in prestashop root element with proper namespace
        root = ET.Element(root_name)
        root.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
        
        for key, value in data.items():
            build_element(root, key, value)
        
        xml_str = ET.tostring(root, encoding='unicode')
        
        # Add XML declaration for complete XML document
        return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'
    
    def _init_multilingual_field(self, value: str = "") -> List[Dict[str, Any]]:
        """Initialize multilingual field for all available languages."""
        return [
            {"id": lang["id"], "value": value}
            for lang in self.available_languages
        ]
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to PrestaShop API."""
        session = await self._get_session()
        url = urljoin(self.base_url, endpoint)
        
        # Always request JSON format for responses
        if params is None:
            params = {}
        params['output_format'] = 'JSON'
        
        # Prepare request body and headers
        request_body = None
        headers = {}
        
        if data and method.upper() in ['POST', 'PUT']:
            # Convert data to XML for write operations
            request_body = self._dict_to_xml(data)
            headers['Content-Type'] = 'application/xml; charset=UTF-8'
            
            # Debug logging for XML structure
            logging.info(f"=== XML Request for {method} {endpoint} ===")
            logging.info(request_body)
            logging.info("=== End XML Request ===")
            
        elif data:
            # For other methods, use JSON (though this should be rare)
            request_body = json.dumps(data)
            headers['Content-Type'] = 'application/json; charset=UTF-8'
        
        try:
            async with session.request(
                method=method,
                url=url,
                params=params,
                data=request_body,
                headers=headers if headers else None
            ) as response:
                if response.status >= 400:
                    error_text = await response.text()
                    raise PrestaShopAPIError(
                        f"API request failed with status {response.status}: {error_text}"
                    )
                
                response_text = await response.text()
                if not response_text:
                    return {}
                
                try:
                    return json.loads(response_text)
                except json.JSONDecodeError:
                    logging.warning(f"Non-JSON response: {response_text}")
                    return {"raw_response": response_text}
        
        except aiohttp.ClientError as e:
            raise PrestaShopAPIError(f"HTTP client error: {str(e)}")

    def _generate_link_rewrite(self, name: str) -> str:
        """Generate URL-friendly link rewrite from name."""
        # Convert to lowercase and replace spaces/special chars with hyphens
        link_rewrite = re.sub(r'[^a-zA-Z0-9\s]', '', name.lower())
        link_rewrite = re.sub(r'\s+', '-', link_rewrite.strip())
        return link_rewrite

    # ============================================================================
    # UNIFIED PRODUCT MANAGEMENT
    # ============================================================================
    
    async def get_products(
        self,
        product_id: Optional[str] = None,
        limit: int = 10,
        filters: Optional[Dict[str, str]] = None,
        include_details: bool = False,
        include_stock: bool = False,
        include_category_info: bool = False,
        display: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Unified product retrieval method supporting all use cases.
        
        Args:
            product_id: Retrieve single product by ID (takes precedence over other params)
            limit: Number of products to retrieve for list queries
            filters: Dictionary of filters (id, name, category)
            include_details: Include complete product information
            include_stock: Include stock/inventory information
            include_category_info: Include category details
            display: Comma-separated list of specific fields to include
            
        Returns:
            Single product data (if product_id provided) or list of products
        """
        
        # Single product by ID
        if product_id:
            return await self._get_single_product(
                product_id=product_id,
                include_details=include_details,
                include_stock=include_stock,
                include_category_info=include_category_info,
                display=display
            )
        
        # Multiple products with optional details
        return await self._get_multiple_products(
            limit=limit,
            filters=filters,
            include_details=include_details,
            include_stock=include_stock,
            include_category_info=include_category_info,
            display=display
        )
    
    async def _get_single_product(
        self,
        product_id: str,
        include_details: bool = False,
        include_stock: bool = False,
        include_category_info: bool = False,
        display: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get single product with optional enhanced information."""
        params = {}
        if display:
            params['display'] = display
        
        try:
            # Get main product data
            product_data = await self._make_request('GET', f'products/{product_id}', params=params)
            
            if 'product' not in product_data:
                raise PrestaShopAPIError(f"Product {product_id} not found")
            
            result = product_data.copy()
            
            # Add enhanced information if requested
            if include_details:
                # Details are already included in the main product data
                pass
            
            if include_stock:
                try:
                    stock_params = {'filter[id_product]': product_id}
                    stock_response = await self._make_request('GET', 'stock_availables', params=stock_params)
                    
                    if 'stock_availables' in stock_response and stock_response['stock_availables']:
                        result['stock_info'] = stock_response['stock_availables'][0]
                    else:
                        result['stock_info'] = {"error": "Stock information not available"}
                        
                except Exception as e:
                    logging.warning(f"Could not retrieve stock info for product {product_id}: {e}")
                    result['stock_info'] = {"error": f"Stock retrieval failed: {str(e)}"}
            
            if include_category_info:
                try:
                    category_id = product_data['product'].get('id_category_default')
                    if category_id:
                        category_response = await self._make_request('GET', f'categories/{category_id}')
                        if 'category' in category_response:
                            result['category_info'] = category_response['category']
                        else:
                            result['category_info'] = {"error": "Category not found"}
                    else:
                        result['category_info'] = {"error": "No default category assigned"}
                        
                except Exception as e:
                    logging.warning(f"Could not retrieve category info for product {product_id}: {e}")
                    result['category_info'] = {"error": f"Category retrieval failed: {str(e)}"}
            
            return result
            
        except PrestaShopAPIError:
            raise
        except Exception as e:
            raise PrestaShopAPIError(f"Failed to retrieve product: {str(e)}")
    
    async def _get_multiple_products(
        self,
        limit: int = 10,
        filters: Optional[Dict[str, str]] = None,
        include_details: bool = False,
        include_stock: bool = False,
        include_category_info: bool = False,
        display: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get multiple products with optional enhanced information."""
        params = {'limit': limit}
        
        if display:
            params['display'] = display
        
        if filters:
            if 'id' in filters:
                params['filter[id]'] = filters['id']
            if 'name' in filters:
                params['filter[name]'] = f"[{filters['name']}]%"
            if 'category' in filters:
                params['filter[id_category_default]'] = filters['category']
        
        products_data = await self._make_request('GET', 'products', params=params)
        
        # If enhanced information is requested, fetch it for each product
        if (include_details or include_stock or include_category_info) and 'products' in products_data:
            enhanced_products = []
            
            for product in products_data['products']:
                product_id = product.get('id')
                if product_id:
                    try:
                        enhanced_product = await self._get_single_product(
                            product_id=product_id,
                            include_details=include_details,
                            include_stock=include_stock,
                            include_category_info=include_category_info,
                            display=display
                        )
                        enhanced_products.append(enhanced_product)
                    except Exception as e:
                        logging.warning(f"Could not enhance product {product_id}: {e}")
                        enhanced_products.append(product)
                else:
                    enhanced_products.append(product)
            
            products_data['products'] = enhanced_products
        
        return products_data
    
    async def create_product(
        self,
        name: str,
        price: float,
        description: Optional[str] = None,
        category_id: Optional[str] = None,
        quantity: Optional[int] = None,
        reference: Optional[str] = None,
        weight: Optional[float] = None
    ) -> Dict[str, Any]:
        """Create a new product in PrestaShop with ALL required fields for backend visibility."""
        link_rewrite = self._generate_link_rewrite(name)
        
        # CRITICAL FIX: Complete product initialization with all required fields
        product_data = {
            "product": {
                # Multilingual fields - properly initialized for all languages
                "name": self._init_multilingual_field(name),
                "link_rewrite": self._init_multilingual_field(link_rewrite),
                "description": self._init_multilingual_field(description if description else ""),
                "description_short": self._init_multilingual_field(
                    description[:160] if description else ""
                ),
                "meta_title": self._init_multilingual_field(name[:70]),
                "meta_description": self._init_multilingual_field(
                    description[:160] if description else name
                ),
                "meta_keywords": self._init_multilingual_field(""),
                
                # CRITICAL: State field for backend visibility (was missing!)
                "state": "1",  # 1 = Published, 0 = Draft (invisible in backend)
                
                # Core product fields
                "price": str(price),
                "active": "1",  # Product is active
                "available_for_order": "1",  # Can be ordered
                "show_price": "1",  # Price is visible
                "indexed": "1",  # Include in search index
                "visibility": "both",  # Visible in catalog and search
                "id_category_default": category_id if category_id else "2",
                
                # Stock and ordering
                "minimal_quantity": "1",
                "low_stock_alert": "0",
                "out_of_stock": "2",  # Deny orders when out of stock
                
                # Physical properties
                "weight": str(weight) if weight is not None else "0",
                "is_virtual": "0",
                
                # System fields
                "cache_default_attribute": "0",
                "id_default_image": "0",
                "id_default_combination": "0",
                "id_tax_rules_group": "1",  # Default tax group
                "id_shop_default": "1",
                "advanced_stock_management": "0",
                "depends_on_stock": "0",
                "pack_stock_type": "3",
                
                # SEO and additional fields
                "redirect_type": "404",
                "id_type_redirected": "0",
                "available_for_order": "1",
                "available_date": "0000-00-00",
                "show_condition": "0",
                "condition": "new",
                "show_price": "1",
                "indexed": "1",
                "visibility": "both",
                "cache_is_pack": "0",
                "public_name": "",
                "cache_has_attachments": "0",
                "is_customizable": "0",
                "uploadable_files": "0",
                "text_fields": "0"
            }
        }
        
        if reference:
            product_data["product"]["reference"] = reference
        
        result = await self._make_request('POST', 'products', data=product_data)
        
        # Handle stock separately if quantity is provided
        if quantity is not None and 'product' in result and 'id' in result['product']:
            product_id = result['product']['id']
            try:
                await self.update_product_stock(product_id, quantity)
            except Exception as e:
                logging.warning(f"Product created but stock update failed: {e}")
        
        return result
    
    async def update_product(
        self, 
        product_id: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Update an existing product in PrestaShop."""
        # First get the existing product
        existing = await self._make_request('GET', f'products/{product_id}')
        
        if 'product' not in existing:
            raise PrestaShopAPIError(f"Product {product_id} not found")
        
        product_data = existing['product']
        
        # Update fields with correct multilingual structure
        if 'name' in kwargs:
            product_data['name'] = self._init_multilingual_field(kwargs['name'])
            link_rewrite = self._generate_link_rewrite(kwargs['name'])
            product_data['link_rewrite'] = self._init_multilingual_field(link_rewrite)
        if 'price' in kwargs:
            product_data['price'] = str(kwargs['price'])
        if 'description' in kwargs:
            product_data['description'] = self._init_multilingual_field(kwargs['description'])
        if 'category_id' in kwargs:
            product_data['id_category_default'] = kwargs['category_id']
        if 'active' in kwargs:
            product_data['active'] = "1" if kwargs['active'] else "0"
        
        return await self._make_request(
            'PUT', 
            f'products/{product_id}', 
            data={"product": product_data}
        )
    
    async def delete_product(self, product_id: str) -> Dict[str, Any]:
        """Delete a product from PrestaShop."""
        return await self._make_request('DELETE', f'products/{product_id}')
    
    async def update_product_stock(
        self, 
        product_id: str, 
        quantity: int
    ) -> Dict[str, Any]:
        """Update product stock quantity with CORRECT XML structure."""
        # Get stock availables for this product
        stock_params = {'filter[id_product]': product_id}
        stock_response = await self._make_request('GET', 'stock_availables', params=stock_params)
        
        if 'stock_availables' in stock_response and stock_response['stock_availables']:
            stock_entry = stock_response['stock_availables'][0]
            stock_id = stock_entry['id']
            
            # CRITICAL FIX: Proper XML structure for stock_available
            stock_data = {
                "stock_available": {
                    "id": str(stock_id),
                    "id_product": str(product_id),
                    "id_product_attribute": "0",  # 0 for simple products
                    "id_shop": "1",  # Default shop
                    "id_shop_group": "0",
                    "quantity": str(quantity),
                    "depends_on_stock": "0",
                    "out_of_stock": "2"  # Deny orders when out of stock
                }
            }
            
            return await self._make_request('PUT', f'stock_availables/{stock_id}', data=stock_data)
        else:
            raise PrestaShopAPIError(f"Stock information not found for product {product_id}")
    
    async def update_product_price(
        self, 
        product_id: str, 
        price: float,
        wholesale_price: Optional[float] = None
    ) -> Dict[str, Any]:
        """Update product price."""
        update_data = {'price': price}
        if wholesale_price is not None:
            update_data['wholesale_price'] = wholesale_price
        
        return await self.update_product(product_id, **update_data)

    # ============================================================================
    # CATEGORY MANAGEMENT
    # ============================================================================
    
    async def get_categories(
        self, 
        limit: int = 10,
        parent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get categories from PrestaShop."""
        params = {'limit': limit}
        
        if parent_id:
            params['filter[id_parent]'] = parent_id
        
        return await self._make_request('GET', 'categories', params=params)
    
    async def create_category(
        self,
        name: str,
        description: Optional[str] = None,
        parent_id: str = "2",
        active: bool = True,
        link_rewrite: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new category in PrestaShop with proper multilingual initialization."""
        if not link_rewrite:
            link_rewrite = self._generate_link_rewrite(name)
        
        # ENHANCED: Complete multilingual field initialization
        category_data = {
            "category": {
                "name": self._init_multilingual_field(name),
                "link_rewrite": self._init_multilingual_field(link_rewrite),
                "description": self._init_multilingual_field(description if description else ""),
                "meta_title": self._init_multilingual_field(name[:70]),
                "meta_description": self._init_multilingual_field(
                    description[:160] if description else name
                ),
                "meta_keywords": self._init_multilingual_field(""),
                "id_parent": parent_id,
                "active": "1" if active else "0",
                "is_root_category": "0",
                "position": "0",
                "date_add": "",
                "date_upd": ""
            }
        }
        
        return await self._make_request('POST', 'categories', data=category_data)
    
    async def update_category(
        self, 
        category_id: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Update an existing category in PrestaShop."""
        # First get the existing category
        existing = await self._make_request('GET', f'categories/{category_id}')
        
        if 'category' not in existing:
            raise PrestaShopAPIError(f"Category {category_id} not found")
        
        # Create minimal category data with only writable core fields
        category_data = {
            "id": str(category_id),
            "id_parent": existing['category'].get('id_parent', '2'),
            "active": existing['category'].get('active', '1'),
            "name": existing['category'].get('name', []),
            "link_rewrite": existing['category'].get('link_rewrite', []),
            "description": existing['category'].get('description', [])
        }
        
        # Update only the requested fields with correct multilingual structure
        if 'name' in kwargs:
            category_data['name'] = self._init_multilingual_field(kwargs['name'])
            link_rewrite = self._generate_link_rewrite(kwargs['name'])
            category_data['link_rewrite'] = self._init_multilingual_field(link_rewrite)
        
        if 'description' in kwargs:
            category_data['description'] = self._init_multilingual_field(kwargs['description'])
        
        if 'active' in kwargs:
            category_data['active'] = "1" if kwargs['active'] else "0"
        
        return await self._make_request(
            'PUT', 
            f'categories/{category_id}', 
            data={"category": category_data}
        )
    
    async def delete_category(self, category_id: str) -> Dict[str, Any]:
        """Delete a category from PrestaShop."""
        return await self._make_request('DELETE', f'categories/{category_id}')

    # ============================================================================
    # CUSTOMER MANAGEMENT
    # ============================================================================
    
    async def get_customers(
        self, 
        limit: int = 10, 
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get customers from PrestaShop."""
        params = {'limit': limit}
        
        if email:
            params['filter[email]'] = f"[{email}]%"
        
        return await self._make_request('GET', 'customers', params=params)
    
    async def create_customer(
        self,
        email: str,
        firstname: str,
        lastname: str,
        password: str,
        active: bool = True
    ) -> Dict[str, Any]:
        """Create a new customer in PrestaShop."""
        customer_data = {
            "customer": {
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
                "passwd": password,
                "active": "1" if active else "0",
                "id_default_group": "3"  # Default customer group
            }
        }
        
        return await self._make_request('POST', 'customers', data=customer_data)
    
    async def update_customer(
        self, 
        customer_id: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Update an existing customer in PrestaShop."""
        # First get the existing customer
        existing = await self._make_request('GET', f'customers/{customer_id}')
        
        if 'customer' not in existing:
            raise PrestaShopAPIError(f"Customer {customer_id} not found")
        
        # Create minimal customer data with only essential fields
        customer_data = {
            "id": str(customer_id),
            "email": existing['customer'].get('email', ''),
            "firstname": existing['customer'].get('firstname', ''),
            "lastname": existing['customer'].get('lastname', ''),
            "id_default_group": existing['customer'].get('id_default_group', '3'),
            "active": existing['customer'].get('active', '1'),
            "passwd": existing['customer'].get('passwd', ''),
            "secure_key": existing['customer'].get('secure_key', ''),
            "date_add": existing['customer'].get('date_add', ''),
            "date_upd": existing['customer'].get('date_upd', ''),
        }
        
        # Update only the provided fields
        if 'email' in kwargs:
            customer_data['email'] = kwargs['email']
        if 'firstname' in kwargs:
            customer_data['firstname'] = kwargs['firstname']
        if 'lastname' in kwargs:
            customer_data['lastname'] = kwargs['lastname']
        if 'active' in kwargs:
            customer_data['active'] = "1" if kwargs['active'] else "0"
        
        return await self._make_request(
            'PUT', 
            f'customers/{customer_id}', 
            data={"customer": customer_data}
        )

    # ============================================================================
    # ORDER MANAGEMENT
    # ============================================================================
    
    async def get_orders(
        self, 
        limit: int = 10, 
        customer_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get orders from PrestaShop."""
        params = {'limit': limit}
        
        if customer_id:
            params['filter[id_customer]'] = customer_id
        if status:
            params['filter[current_state]'] = status
        
        return await self._make_request('GET', 'orders', params=params)
    
    async def update_order_status(
        self, 
        order_id: str, 
        status_id: str
    ) -> Dict[str, Any]:
        """Update order status in PrestaShop."""
        # Create order history entry
        history_data = {
            "order_history": {
                "id_order": order_id,
                "id_order_state": status_id,
                "id_employee": "1"  # Default employee
            }
        }
        
        return await self._make_request('POST', 'order_histories', data=history_data)
    
    async def get_order_states(self) -> Dict[str, Any]:
        """Retrieve available order states/statuses."""
        return await self._make_request('GET', 'order_states')

    # ============================================================================
    # CONFIGURATION AND UTILITY
    # ============================================================================
    
    async def get_configurations(
        self, 
        filter_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get shop configurations from PrestaShop."""
        params = {}
        
        if filter_name:
            params['filter[name]'] = f"[{filter_name}]%"
        
        return await self._make_request('GET', 'configurations', params=params)
    
    async def get_shop_info(self) -> Dict[str, Any]:
        """Get general shop information and statistics."""
        try:
            # Get basic shop info
            configs = await self.get_configurations()
            
            # Get product count
            products = await self._make_request('GET', 'products', params={'limit': 1})
            product_count = 0
            if 'products' in products:
                product_count = len(products.get('products', []))
            
            # Get category count
            categories = await self._make_request('GET', 'categories', params={'limit': 1})
            category_count = 0
            if 'categories' in categories:
                category_count = len(categories.get('categories', []))
            
            # Get customer count
            customers = await self._make_request('GET', 'customers', params={'limit': 1})
            customer_count = 0
            if 'customers' in customers:
                customer_count = len(customers.get('customers', []))
            
            # Get order count
            orders = await self._make_request('GET', 'orders', params={'limit': 1})
            order_count = 0
            if 'orders' in orders:
                order_count = len(orders.get('orders', []))
            
            return {
                "shop_info": {
                    "product_count": product_count,
                    "category_count": category_count,
                    "customer_count": customer_count,
                    "order_count": order_count
                },
                "configurations": configs
            }
        
        except Exception as e:
            return {"error": f"Could not retrieve shop info: {str(e)}"}
    
    # ============================================================================
    # SESSION MANAGEMENT
    # ============================================================================
    
    async def close(self):
        """Close the HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
