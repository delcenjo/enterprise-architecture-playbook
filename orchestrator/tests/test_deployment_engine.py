import unittest
import os
import sys

# Mock setup for standalone testing
from global_state import GlobalState, ArchitectureSpec
from layers.core_engine import CoreEngine

class TestDeploymentEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_fintech_blue_green(self):
        """Verify that a critical fintech system gets Blue-Green deployment."""
        self.state.raw_input = {
            "business_type": "FINTECH_HA",
            "payment_operations_enabled": True
        }
        # In core_engine, is_psd2_scope is triggered by business_type "FINTECH"
        # latency_critical is triggered by FINTECH (forces 200ms)
        # large_scale is triggered by concurrent_users > 50000
        
        # We need is_bde_supervised or large_scale for Blue-Green
        self.state.raw_input["is_bde_supervised"] = True
        
        self.engine.run_layer_2()
        
        deploy = self.engine.state.architecture.deployment
        self.assertEqual(deploy["strategy"], "Blue-Green Deployment")
        self.assertEqual(deploy["tier"], "recommend_blue_green")

    def test_high_scale_canary(self):
        """Verify that a high-scale system gets Canary deployment."""
        self.state.raw_input = {
            "business_type": "SAAS_STANDARD",
        }
        # large_scale = True triggers Canary check after root=No
        self.state.traffic_profile.concurrent_users = 100000 
        
        self.engine.run_layer_2()
        
        deploy = self.engine.state.architecture.deployment
        # root=No because not PSD2 and not latency_critical (SaaS != Fintech)
        # canary_check=Yes because large_scale or microservices
        self.assertEqual(deploy["strategy"], "Canary Deployment")
        self.assertEqual(deploy["tier"], "recommend_canary")

    def test_multi_tenant_feature_flags(self):
        """Verify that a standard multi-tenant SaaS gets Feature Flags."""
        self.state.raw_input = {
            "business_type": "SAAS_STANDARD",
        }
        self.state.traffic_profile.concurrent_users = 1000 # scaling_problem=True, but not large_scale
        
        self.engine.run_layer_2()
        
        deploy = self.engine.state.architecture.deployment
        # root=No, canary_check=No (not large_scale, 1 component default?), 
        # feature_flag_check=Yes (multi_tenant is True for SAAS)
        self.assertEqual(deploy["strategy"], "Feature Flags / Dark Launches")
        self.assertEqual(deploy["tier"], "recommend_feature_flags")

    def test_startup_rolling(self):
        """Verify that a lean startup gets standard rolling update."""
        self.state.raw_input = {
            "business_type": "STARTUP_MVP"
        }
        # No large scale, no multi-tenant (Gini is 0.4)
        
        self.engine.run_layer_2()
        
        deploy = self.engine.state.architecture.deployment
        self.assertEqual(deploy["strategy"], "Standard Rolling Update")
        self.assertEqual(deploy["tier"], "recommend_standard_rolling")

if __name__ == "__main__":
    unittest.main()
