import json
import os
import logging
from typing import Dict, Any
from global_state import GlobalState, FinancialModel

# Import New Core Modules
from core.workload_model import WorkloadModel
from core.resource_estimator import ResourceEstimator
from core.pricing_engine import PricingEngine
from core.scenario_simulator import ScenarioSimulator

logger = logging.getLogger("Layer3_CalcEngine_V3")
logging.basicConfig(level=logging.INFO)

class CalculationEngine:
    def __init__(self, state: GlobalState):
        self.state = state
        self.pricing_path = os.path.join(os.path.dirname(__file__), "..", "assets", "pricing", "aws.json")
        self.meta_path = os.path.join(os.path.dirname(__file__), "..", "assets", "region_metadata.json")

    def run_layer_3(self):
        """
        Layer 3: Deterministic Financial Orchestrator (V3 Global)
        1. Multi-Region Context Loading
        2. Workload Modeling with Environmental Factors
        3. Multi-Provider Pricing & Currency Conversion
        4. Comparison & Simulation
        """
        logger.info("Orchestrating Global Engineering-First Financial Models...")
        
        # 1. Load Data
        with open(self.pricing_path, 'r') as f:
            pricing_data = json.load(f)
        with open(self.meta_path, 'r') as f:
            region_meta = json.load(f)

        region = self.state.compliance_profile.required_region
        meta_entry = region_meta["regions"].get(region, region_meta["regions"]["us-east-1"])

        # 2. Workload Modeling (Injection of Latency Penalty)
        workload_engine = WorkloadModel(self.state.raw_input)
        workload = workload_engine.calculate_load_profile(meta_entry["environmental_factors"])
        self.state.traffic_profile.egress_gb_month = workload['monthly_egress_gb']
        
        # 3. Resource Estimation
        requirements = ResourceEstimator(workload).estimate_requirements()
        
        # 4. Pricing Engine (Multi-Provider & Currency)
        pricing_engine = PricingEngine(pricing_data, region_meta, region)
        
        # Preferred Provider (AWS by default or from input)
        preferred = self.state.raw_input.get("preferred_provider", "aws").lower()
        costs = pricing_engine.calculate_total_monthly(requirements, preferred)
        
        # Comparison Audit
        comparison = pricing_engine.compare_providers(requirements)
        
        # 5. Financial Simulation
        simulator = ScenarioSimulator(costs['total_local'], self.state.traffic_profile.growth_rate)
        scenarios = simulator.run_simulation()
        npv = simulator.calculate_npv(scenarios['Base'])
        
        # Update Global State
        self.state.costs["total_monthly"] = costs['total_local']
        self.state.costs["currency"] = costs['currency']
        self.state.costs["currency_symbol"] = costs['currency_symbol']
        self.state.costs["provider_comparison"] = comparison
        self.state.costs["resource_breakdown"] = costs['breakdown']
        self.state.costs["raw_requirements"] = requirements
        
        self.state.financial_model = FinancialModel(
            cloud_costs={"total_monthly": costs['total_local'], "total_yearly": costs['total_local'] * 12},
            usage_breakdown=costs['breakdown'],
            npv=npv,
            roi_months=6,
            scenarios=scenarios
        )

        logger.info(f"V3 Global Calculation Complete. TCO: {costs['currency_symbol']}{costs['total_local']:,.2f} ({costs['currency']})")
        return f"Global financial modeling complete for {region} ({costs['currency']})"

if __name__ == "__main__":
    pass
