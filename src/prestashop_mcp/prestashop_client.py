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
                # <n><language id="1">value</language><language id="2">value</language></n>
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
        
        root = ET.Element(root_name)
        for key, value in data.items():
            build_element(root, key, value)
        
        return ET.tostring(root, encoding='unicode')
    
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
            headers['Content-Type'] = 'application/xml'
            
            # Debug logging for XML structure
            logging.info(f"=== XML Request for {method} {endpoint} ===")
            logging.info(request_body)
            logging.info("=== End XML Request ===")
            
        elif data:
            # For other methods, use JSON (though this should be rare)
            request_body = json.dumps(data)
            headers['Content-Type'] = 'application/json'
        
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
    # PRODUCT MANAGEMENT
    # ============================================================================
    
    async def get_products(
        self, 
        limit: int = 10, 
        filters: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Get products from PrestaShop."""
        params = {'limit': limit}
        
        if filters:
            if 'id' in filters:
                params['filter[id]'] = filters['id']
            if 'name' in filters:
                params['filter[name]'] = f"[{filters['name']}]%"
            if 'category' in filters:
                params['filter[id_category_default]'] = filters['category']
        
        return await self._make_request('GET', 'products', params=params)
    
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
        """Create a new product in PrestaShop with FINAL corrected structure."""
        link_rewrite = self._generate_link_rewrite(name)
        
        # CRITICAL FIX: Remove "quantity" field - it's not writable in products!
        # Quantity is managed separately via stock_availables API
        product_data = {
            "product": {
                # Basic identification
                "name": [
                    {"id": 1, "value": name},
                    {"id": 2, "value": name}
                ],
                "link_rewrite": [
                    {"id": 1, "value": link_rewrite},
                    {"id": 2, "value": link_rewrite}
                ],
                
                # Price and basic properties
                "price": str(price),
                "active": "1",
                "available_for_order": "1",
                "show_price": "1",
                
                # Category assignment
                "id_category_default": category_id if category_id else "2",
                
                # Basic stock settings (NO direct quantity field!)
                "minimal_quantity": "1",
                "low_stock_alert": "0",
                
                # Physical properties with defaults
                "weight": str(weight) if weight is not None else "0",
                "width": "0",
                "height": "0", 
                "depth": "0",
                
                # Essential flags to avoid attribute creation
                "is_virtual": "0",
                "cache_default_attribute": "0",
                "id_default_image": "0",
                
                # Tax and pricing
                "id_tax_rules_group": "1",
                "additional_shipping_cost": "0.00",
                "unit_price": "0.000000",
                "unity": "",
                "unit_price_ratio": "0.000000",
                "ecotax": "0.000000",
                
                # Behavior flags
                "customizable": "0",
                "uploadable_files": "0", 
                "text_fields": "0",
                "out_of_stock": "2",
                "depends_on_stock": "0",
                "advanced_stock_management": "0",
                
                # SEO and display
                "indexed": "1",
                "visibility": "both",
                "condition": "new",
                "show_condition": "0",
                "online_only": "0",
                
                # Dates and status
                "available_date": "0000-00-00",
                "date_add": "",
                "date_upd": "",
                
                # Pack and attachment flags
                "cache_is_pack": "0",
                "cache_has_attachments": "0",
                "is_pack": "0",
                
                # Redirect
                "redirect_type": "404",
                "id_type_redirected": "0",
                
                # Manufacturer and supplier
                "id_manufacturer": "0",
                "id_supplier": "0",
                
                # Multi-language fields with empty defaults
                "description": [
                    {"id": 1, "value": description if description else ""},
                    {"id": 2, "value": description if description else ""}
                ],
                "description_short": [
                    {"id": 1, "value": description[:160] if description else ""},
                    {"id": 2, "value": description[:160] if description else ""}
                ],
                "available_now": [
                    {"id": 1, "value": ""},
                    {"id": 2, "value": ""}
                ],
                "available_later": [
                    {"id": 1, "value": ""},
                    {"id": 2, "value": ""}
                ],
                "meta_description": [
                    {"id": 1, "value": ""},
                    {"id": 2, "value": ""}
                ],
                "meta_keywords": [
                    {"id": 1, "value": ""},
                    {"id": 2, "value": ""}
                ],
                "meta_title": [
                    {"id": 1, "value": name[:70]},
                    {"id": 2, "value": name[:70]}
                ]
            }
        }
        
        # Set reference if provided
        if reference:
            product_data["product"]["reference"] = reference
        
        # Add category associations if specified
        if category_id:
            product_data["product"]["associations"] = {
                "categories": {
                    "category": {
                        "id": category_id
                    }
                }
            }
        
        # Create product first
        result = await self._make_request('POST', 'products', data=product_data)
        
        # SEPARATELY handle stock if quantity is provided
        if quantity is not None and 'product' in result and 'id' in result['product']:
            product_id = result['product']['id']
            try:
                await self.update_product_stock(product_id, quantity)
            except Exception as e:
                # Log stock update error but don't fail the product creation
                logging.warning(f"Product created but stock update failed: {e}")
        
        return result