import unittest
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Set PYTHONPATH to include orchestrator
os.environ["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + ":" + os.environ.get("PYTHONPATH", "")

from orchestrator.global_state import GlobalState
from orchestrator.layers.core_engine import CoreEngine

class TestGDPRCrossBorder(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_transfer_to_us_high_risk(self):
        """Verify TIA and supplementary measures for US transfer."""
        self.state.raw_input = {
            "business_type": "FINTECH",
            "destination_country": "US",
            "pii_operations_needed": True
        }
        self.state.compliance_profile.frameworks = ["GDPR"]
        
        self.engine.run_layer_2()
        
        transfer = self.state.architecture.transfer_assessment
        self.assertTrue(transfer.is_international)
        self.assertEqual(transfer.destination_country, "US")
        self.assertEqual(transfer.jurisdictional_risk_level, "High (FISA 702 Risks)")
        self.assertTrue(transfer.tia_required)
        self.assertIn("EU-Controlled KMS", transfer.supplementary_measures)
        
        # Verify pattern injection
        pattern_ids = [p["id"] for p in self.state.architecture.enterprise_patterns]
        self.assertIn("eu_controlled_keys", pattern_ids)

    def test_transfer_to_uk_adequate(self):
        """Verify UK is treated as adequate with no TIA mandatory (simplified)."""
        self.state.raw_input = {
            "business_type": "SAAS",
            "destination_country": "UK"
        }
        self.state.compliance_profile.frameworks = ["GDPR"]
        
        self.engine.run_layer_2()
        
        transfer = self.state.architecture.transfer_assessment
        # In our simplified logic, UK is NOT cross-border (EEA+UK excluded from is_cross_border)
        self.assertFalse(transfer.is_international) 
        self.assertEqual(transfer.adequacy_status, "Adequate")

    def test_transfer_to_brazil_scc(self):
        """Verify transfer to Brazil requires SCCs."""
        self.state.raw_input = {
            "business_type": "RETAIL",
            "destination_country": "BR"
        }
        self.state.compliance_profile.frameworks = ["GDPR"]
        
        self.engine.run_layer_2()
        
        transfer = self.state.architecture.transfer_assessment
        self.assertTrue(transfer.is_international)
        self.assertEqual(transfer.legal_basis, "Standard Contractual Clauses (SCCs)")
        self.assertEqual(transfer.jurisdictional_risk_level, "Medium")

if __name__ == "__main__":
    unittest.main()
