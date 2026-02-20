import unittest
import os
import sys
from typing import Dict, List, Any

# Mock setup for standalone testing
from global_state import GlobalState, ArchitectureSpec
from layers.core_engine import CoreEngine

class TestChaosEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_fintech_critical_chaos(self):
        """Verify that a critical fintech system gets Production Failure Injection."""
        self.state.raw_input = {
            "business_type": "FINTECH_HA",
            "payment_operations_enabled": True,
            "is_bde_supervised": True # triggers maturity
        }
        # Force large scale to trigger production injection
        self.state.traffic_profile.concurrent_users = 100000 
        
        # Simulate microservices
        self.state.requirements = {"services": ["auth", "payment", "ledger"]}
        
        self.engine.run_layer_2()
        
        chaos = self.engine.state.architecture.chaos
        self.assertEqual(chaos["strategy"], "Production Failure Injection")
        self.assertEqual(chaos["tier"], "recommend_production_failure_injection")
        self.assertIn("Production Chaos", chaos["recommended_pillars"])

    def test_standard_saas_chaos(self):
        """Verify that a standard SAAS gets GameDays simulation."""
        self.state.raw_input = {
            "business_type": "SAAS_STANDARD",
        }
        self.state.traffic_profile.concurrent_users = 10000 # triggers root
        self.state.requirements = {"services": ["app", "worker"]} # triggers microservices
        
        # For SAAS_STANDARD, maturity might be lower than banking
        self.engine.run_layer_2()
        
        chaos = self.engine.state.architecture.chaos
        # By default SAAS_STANDARD with 10k users -> team_maturity = No (not Bde/LargeScale enough?)
        # Wait, large_scale is > 50k in metrics. 
        # So for SAAS_STANDARD with 10k users, it should be staging simulation.
        self.assertEqual(chaos["strategy"], "Simulation in Staging")
        self.assertEqual(chaos["tier"], "recommend_staging_simulation")

    def test_startup_minimal_chaos(self):
        """Verify that a small startup doesn't get chaos engineering."""
        self.state.raw_input = {
            "business_type": "STARTUP_MVP"
        }
        self.state.requirements = {"services": ["api"]} # Monolith
        
        self.engine.run_layer_2()
        
        chaos = self.engine.state.architecture.chaos
        self.assertEqual(chaos["strategy"], "Traditional Testing Only")
        self.assertEqual(chaos["tier"], "recommend_traditional_testing")

if __name__ == "__main__":
    unittest.main()
