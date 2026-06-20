import json
import os
from typing import Dict, Any

class PricingEngine:
    """
    Maps Resource requirements to Local Dollars/EUR using versioned tables and regional metadata.
    Supports AWS, Azure, and GCP comparison.
    """
    def __init__(self, pricing_data: Dict[str, Any], meta: Dict[str, Any], region: str = "us-east-1"):
        self.pricing = pricing_data
        self.meta = meta
        self.region_meta = self.meta["regions"].get(region, self.meta["regions"]["us-east-1"])
        self.currency_info = self.meta["currencies"].get(self.region_meta["currency"], self.meta["currencies"]["USD"])
        
        self.regional_multiplier = self.region_meta["cost_multiplier"]
        self.conversion_rate = self.currency_info["rate_to_usd"]
        self.tax_rate = self.region_meta["tax_rate"]

    def calculate_total_monthly(self, requirements: Dict[str, Any], provider: str = "aws") -> Dict[str, Any]:
        p_info = self.meta["providers"].get(provider, self.meta["providers"]["aws"])
        
        vcpu = requirements['compute']['vcpu']
        units = max(1, vcpu / 2)
        base_compute = units * self.pricing['instances']['m5.large']['hourly_cost'] * 730
        compute_cost = base_compute * p_info["base_index"]

        storage_gb = requirements['storage']['volume_gb']
        storage_cost = storage_gb * self.pricing['storage']['gp3']['per_gb_month']

        extra_iops = max(0, requirements['storage']['iops'] - 3000)
        iops_cost = extra_iops * self.pricing['storage']['gp3']['extra_iops_cost']

        egress_gb = requirements['networking']['egress_gb']
        egress_cost = egress_gb * p_info["egress_discount_tier"]

        subtotal_usd = (compute_cost + storage_cost + iops_cost + egress_cost) * self.regional_multiplier
        
        # Environmental Compliance Penalty (e.g. GDPR audits)
        if self.region_meta["environmental_factors"].get("gdpr_active"):
            subtotal_usd += 500 # $500/mo management overhead
            
        total_usd = subtotal_usd * (1 + self.tax_rate)
        total_local = total_usd * self.conversion_rate
        
        return {
            "total_local": total_local,
            "total_usd": total_usd,
            "currency": self.region_meta["currency"],
            "currency_symbol": self.currency_info["symbol"],
            "breakdown": {
                "compute": compute_cost * self.regional_multiplier * (1 + self.tax_rate) * self.conversion_rate,
                "storage": (storage_cost + iops_cost) * self.regional_multiplier * (1 + self.tax_rate) * self.conversion_rate,
                "networking": egress_cost * self.regional_multiplier * (1 + self.tax_rate) * self.conversion_rate
            },
            "raw_metrics": requirements
        }

    def compare_providers(self, requirements: Dict[str, Any]) -> Dict[str, float]:
        return {p: self.calculate_total_monthly(requirements, p)["total_local"] for p in self.meta["providers"].keys()}
