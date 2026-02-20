import unittest
import json
import os
import sys

# Ensure orchestrator is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestSREEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_fintech_critical_sre(self):
        """Verify that a critical fintech system gets strict SLOs and SLAs."""
        print("\nRunning test_fintech_critical_sre...")
        self.state.raw_input = {
            "business_type": "FINTECH_HA",
            "payment_operations_enabled": True, # PSD2 scope
            "is_bde_supervised": True # Strict SLO
        }
        
        self.engine.run_layer_2()
        print("Layer 2 complete.")
        
        rel = self.engine.state.architecture.reliability
        self.assertEqual(rel["reliability_tier"], "leaf_strict_slo_sla")
        self.assertEqual(rel["slo_target"], 99.95)
        self.assertTrue(rel["sla_active"])
        self.assertIn("Burn Rate Alerts", rel["features"])
        
        # Verify SLIs
        sli_names = [s["concepto"] for s in rel["slis"]]
        self.assertIn("SLI", sli_names) # Latency is SLI
        self.assertIn("SLO", sli_names) # Availability is SLO

    def test_moderate_startup_sre(self):
        """Verify that a small startup gets moderate SLOs and no SLA."""
        self.state.raw_input = {
            "business_type": "SAAS_STANDARD",
            "is_gdpr_critical": True # Moderate alerting
        }
        
        self.engine.run_layer_2()
        
        rel = self.engine.state.architecture.reliability
        self.assertEqual(rel["reliability_tier"], "leaf_moderate_slo_alerting")
        self.assertEqual(rel["slo_target"], 99.0)
        self.assertFalse(rel["sla_active"])

    def test_basic_env_sre(self):
        """Verify basic environment gets Reporting Only."""
        self.state.raw_input = {
            "business_type": "DEV_ENV"
        }
        
        self.engine.run_layer_2()
        
        rel = self.engine.state.architecture.reliability
        self.assertEqual(rel["reliability_tier"], "leaf_basic_metrics")
        self.assertEqual(rel["slo_target"], 95.0)

if __name__ == "__main__":
    unittest.main()
