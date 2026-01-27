import numpy as np
from typing import Dict, List, Any

class ScenarioSimulator:
    """
    Pure math for 5-Year projections and NPV.
    """
    def __init__(self, base_monthly: float, growth_rate: float):
        self.base_monthly = base_monthly
        self.growth_rate = growth_rate

    def run_simulation(self) -> Dict[str, List[float]]:
        months = np.arange(60)
        
        def project(rate_adj):
            # linear growth for simplicity, or compound
            return [self.base_monthly * (1 + (self.growth_rate * rate_adj) * (m / 12)) for m in months]

        return {
            "Base": project(1.0),
            "Optimistic": project(1.5),
            "Conservative": project(0.5)
        }

    def calculate_npv(self, cash_flows: List[float], discount_rate: float = 0.1) -> float:
        rate_monthly = discount_rate / 12
        # Assume benefit is 3x cost for NPV simulation
        net_flows = [(cf * 3) - cf for cf in cash_flows]
        return sum(cf / (1 + rate_monthly)**t for t, cf in enumerate(net_flows))
