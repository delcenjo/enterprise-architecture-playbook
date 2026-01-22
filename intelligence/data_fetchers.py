import os
import requests
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

PRICING_API_URL = os.environ.get("PRICING_API_URL", "http://api:8000")

class PricingFetcher:
    def __init__(self):
        self.base_url = PRICING_API_URL

    def get_ec2_cost(self, instance_type: str, region: str, os_name: str = "Linux", hours: int = 730) -> Dict[str, Any]:
        """
        Consulta la API de precios de la Capa 2 (Knowledge) para obtener un dato verificado y anclado.
        """
        url = f"{self.base_url}/calculate"
        payload = {
            "instance_type": instance_type,
            "region": region,
            "hours_per_month": hours,
            "operating_system": os_name
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching pricing data: {e}")
            raise RuntimeError(f"Failed to fetch grounded pricing data for {instance_type} in {region}") from e
