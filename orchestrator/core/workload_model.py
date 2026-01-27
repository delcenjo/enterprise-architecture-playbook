from typing import Dict, Any

class WorkloadModel:
    """
    Transforms Business Metrics into Technical Load Profiles.
    Pure math, no AI.
    """
    def __init__(self, raw_input: Dict[str, Any]):
        self.raw_input = raw_input

    def calculate_load_profile(self, env_factors: Dict[str, Any] = None) -> Dict[str, float]:
        expected_users = float(self.raw_input.get("expected_users_year1", 10000))
        rps_per_user = float(self.raw_input.get("rps_per_user", 0.01))
        avg_payload_kb = float(self.raw_input.get("avg_payload_kb", 50))
        
        latency_multiplier = env_factors.get("latency_penalty", 1.0) if env_factors else 1.0
        
        # Calculations
        peak_rps = (expected_users * rps_per_user) * 3.0 * latency_multiplier
        daily_requests = expected_users * rps_per_user * 3600 * 24
        monthly_egress_gb = (daily_requests * avg_payload_kb * 30 * latency_multiplier) / (1024 * 1024)
        
        return {
            "peak_rps": peak_rps,
            "avg_rps": (expected_users * rps_per_user) * latency_multiplier,
            "monthly_egress_gb": monthly_egress_gb,
            "daily_requests": daily_requests,
            "latency_factor": latency_multiplier
        }
