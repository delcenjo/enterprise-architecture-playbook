from typing import Dict, Any

class ResourceEstimator:
    """
    Maps Technical Load Profiles to Physical/Resource requirements.
    """
    def __init__(self, load_profile: Dict[str, float]):
        self.load = load_profile

    def estimate_requirements(self) -> Dict[str, Any]:
        # Benchmarks: 1 vCPU can handle ~200 RPS of standard API load
        # 1 GB RAM per 500 concurrent connections
        
        vcpu_needed = max(2, self.load['peak_rps'] / 200)
        ram_gb_needed = max(4, (self.load['peak_rps'] / 500) * 2) # Security buffer
        
        # IOPS Base (e.g. 500 IOPS per 100 RPS)
        iops_needed = max(3000, (self.load['avg_rps'] / 100) * 500)
        
        return {
            "compute": {
                "vcpu": vcpu_needed,
                "ram_gb": ram_gb_needed
            },
            "storage": {
                "iops": iops_needed,
                "volume_gb": self.load['monthly_egress_gb'] * 0.5 # Data retention heuristic
            },
            "networking": {
                "egress_gb": self.load['monthly_egress_gb']
            }
        }
