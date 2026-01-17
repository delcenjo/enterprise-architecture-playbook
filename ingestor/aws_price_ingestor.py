import json
import hashlib
from datetime import datetime
from typing import Dict, List
import urllib.request
import gzip

class AWSPriceIngestor:
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        # Usamos la API pública de AWS Price Bulk:
        # Nota: El archivo entero puede ser masivo (GBs descomprimidos), pero solo hay un endpoint 
        # alternativo index.json por region si queremos saltarnos la credencial boto3
        self.pricing_url = f"https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/eu-west-1/index.json"
        
    def fetch_all_prices(self, service_code: str = 'AmazonEC2', target_region: str = 'EU (Ireland)') -> Dict:
        """
        Descarga todos los precios de un servicio (ej: EC2) para una región específica leyendo el Bulk JSON.
        """
        print(f"Fetching {service_code} prices via public URL: {self.pricing_url}")
        
        req = urllib.request.Request(self.pricing_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data_bytes = response.read()
            data = json.loads(data_bytes.decode('utf-8'))
            
        products = data.get('products', {})
        terms = data.get('terms', {}).get('OnDemand', {})
        
        all_products = []
        instance_types_to_fetch = ["t3.micro", "t3.medium", "m5.large"]
        
        count = 0
        for sku, product_obj in products.items():
            attrs = product_obj.get('attributes', {})
            instance_type = attrs.get('instanceType', '')
            tenancy = attrs.get('tenancy', '')
            os_name = attrs.get('operatingSystem', '')
            capacity = attrs.get('capacitystatus', '')
            
            if (instance_type in instance_types_to_fetch and 
                tenancy == 'Shared' and 
                os_name == 'Linux' and 
                capacity == 'Used'):
                
                # Adjuntar terms (el precio) al product obj para hacerlo compatible con la logica previa
                product_terms = {}
                if sku in terms:
                    product_terms['OnDemand'] = terms[sku]
                
                combined_product = {
                    "product": product_obj,
                    "terms": product_terms
                }
                
                all_products.append(combined_product)
                count += 1
                
        print(f"Found {count} products matching filters.")

        return {
            'service': service_code,
            'region': target_region,
            'count': len(all_products),
            'ingested_at': datetime.utcnow().isoformat(),
            'checksum': self._calculate_checksum(all_products),
            'data': all_products
        }
    
    def _calculate_checksum(self, data: List[Dict]) -> str:
        """Para detectar cambios entre ejecuciones completas (opcional)"""
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()

    def extract_hourly_price(self, product: Dict) -> float:
        """Extrae el precio OnDemand por hora del JSON """
        terms = product.get('terms', {})
        on_demand = terms.get('OnDemand', {})
        if not on_demand:
            return 0.0
            
        first_offer_key = list(on_demand.keys())[0]
        offer_term = on_demand.get(first_offer_key, {})
        price_dims = offer_term.get('priceDimensions', {})
        
        if not price_dims:
            return 0.0
            
        first_dim_key = list(price_dims.keys())[0]
        dim = price_dims.get(first_dim_key, {})
        price_per_unit = dim.get('pricePerUnit', {}).get('USD', '0.0')
        
        try:
            return float(price_per_unit)
        except ValueError:
            return 0.0

    def parse_product(self, product: Dict) -> Dict:
        """Transforma la estructura de AWS en campos planitos para la DB"""
        attrs = product.get('product', {}).get('attributes', {})
        sku = product.get('product', {}).get('sku', '')
        
        # Parse numbers robustly
        vcpus_str = attrs.get('vcpu', '0')
        mem_str = attrs.get('memory', '0 GiB').split(' ')[0]
        try:
            vcpus = int(vcpus_str)
        except ValueError:
            vcpus = 0
            
        try:
            memory_gb = float(mem_str)
        except ValueError:
            memory_gb = 0.0
            
        price_per_hour = self.extract_hourly_price(product)
        
        return {
            "sku": sku,
            "service_code": attrs.get('servicecode', 'AmazonEC2'),
            "region_code": 'eu-west-1', # Hardcoded for mapping EU (Ireland) for now
            "instance_type": attrs.get('instanceType', ''),
            "vcpus": vcpus,
            "memory_gb": memory_gb,
            "operating_system": attrs.get('operatingSystem', 'Linux'),
            "tenancy": attrs.get('tenancy', 'Shared'),
            "price_per_hour": price_per_hour,
            "currency": 'USD',
            "raw_json": json.dumps(product)
        }
