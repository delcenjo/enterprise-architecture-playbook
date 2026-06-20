import unittest
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Set PYTHONPATH to include orchestrator
os.environ["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + ":" + os.environ.get("PYTHONPATH", "")

from orchestrator.global_state import GlobalState
from orchestrator.layers.core_engine import CoreEngine

class TestBdEGovernance(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_bde_supervised_fintech(self):
        """Verify BdE governance for a supervised Fintech entity."""
        self.state.raw_input = {
            "business_type": "FINTECH",
            "pii_operations_needed": True,
            "tags": ["Banking"]
        }
        
        self.engine.run_layer_2()
        
        self.assertTrue(self.state.bde_governance.is_supervised_entity)
        self.assertEqual(self.state.bde_governance.board_approval_status, "Mandatory")
        self.assertTrue(self.state.bde_governance.operational_risk_mapping)

        audit_controls = [item["control"] for item in self.state.technical_audit]
        self.assertIn("Financial Control", audit_controls)

        pattern_ids = [p["id"] for p in self.state.architecture.enterprise_patterns]
        self.assertIn("isolated_financial_segment", pattern_ids)
        self.assertIn("dual_control_op", pattern_ids)

        subnets = self.state.architecture.networking["subnets"]
        financial_subnet = next((s for s in subnets if s.get("purpose") == "BdE Circular 4/2017 Compliance"), None)
        self.assertIsNotNone(financial_subnet, "Financial subnet should be present")
        if financial_subnet:
            self.assertEqual(financial_subnet["tier"], "isolated")


    def test_non_supervised_startup(self):
        """Verify that BdE patterns are NOT applied to non-supervised startups."""
        self.state.raw_input = {
            "business_type": "STARTUP",
            "pii_operations_needed": False
        }
        
        self.engine.run_layer_2()
        
        self.assertFalse(self.state.bde_governance.is_supervised_entity)

        pattern_ids = [p["id"] for p in self.state.architecture.enterprise_patterns]
        self.assertNotIn("isolated_financial_segment", pattern_ids)
        self.assertNotIn("dual_control_op", pattern_ids)

if __name__ == "__main__":
    unittest.main()
