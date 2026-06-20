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
        # Blue-Green requires is_bde_supervised or large_scale
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
        self.state.traffic_profile.concurrent_users = 100000  # large_scale=True triggers Canary

        self.engine.run_layer_2()

        deploy = self.engine.state.architecture.deployment
        self.assertEqual(deploy["strategy"], "Canary Deployment")
        self.assertEqual(deploy["tier"], "recommend_canary")

    def test_multi_tenant_feature_flags(self):
        """Verify that a standard multi-tenant SaaS gets Feature Flags."""
        self.state.raw_input = {
            "business_type": "SAAS_STANDARD",
        }
        self.state.traffic_profile.concurrent_users = 1000  # not large_scale; multi_tenant triggers feature flags

        self.engine.run_layer_2()

        deploy = self.engine.state.architecture.deployment
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
