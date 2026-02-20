import unittest
import json
import os
import sys

# Ensure orchestrator is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestCNMVCompliance(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_crowdfunding_ecsp_flow(self):
        """Verify Crowdfunding platform triggers ECSP patterns (classification, cooling-off)."""
        self.state.raw_input = {
            "business_type": "CROWDFUNDING",
            "target_retail_customers": True
        }
        self.engine.run_layer_2()
        
        cnmv = self.state.cnmv_compliance
        self.assertTrue(cnmv.is_in_scope)
        self.assertEqual(cnmv.investment_type, "crowdfunding")
        self.assertTrue(cnmv.investment_config.investor_classification_automated)
        self.assertTrue(cnmv.investment_config.cooling_off_period_enforced)
        
        # Check Patterns
        pattern_ids = [p["id"] for p in self.state.architecture.enterprise_patterns]
        self.assertIn("crowdfunding_escrow_segregation", pattern_ids)

    def test_roboadvisor_mifid_flow(self):
        """Verify Roboadvisor triggers MiFID II suitability and explainability."""
        self.state.raw_input = {
            "business_type": "ROBOADVISOR",
            "target_retail_customers": True
        }
        self.engine.run_layer_2()
        
        cnmv = self.state.cnmv_compliance
        self.assertTrue(cnmv.is_in_scope)
        self.assertEqual(cnmv.investment_type, "roboadvisor")
        self.assertTrue(cnmv.investment_config.suitability_test_structured)
        self.assertTrue(cnmv.investment_config.algorithmic_explainability)
        
        # Check Patterns
        pattern_ids = [p["id"] for p in self.state.architecture.enterprise_patterns]
        self.assertIn("investor_suitability_hub", pattern_ids)
        self.assertIn("market_abuse_monitoring", pattern_ids)

    def test_crypto_mica_custody_flow(self):
        """Verify Crypto CASP with custody triggers MiCA and hardened HSM."""
        self.state.raw_input = {
            "business_type": "CRYPTO_EXCHANGE",
            "custody_enabled": True
        }
        self.engine.run_layer_2()
        
        cnmv = self.state.cnmv_compliance
        self.assertTrue(cnmv.is_in_scope)
        self.assertEqual(cnmv.investment_type, "crypto")
        self.assertTrue(cnmv.crypto_config.cold_storage_hsm)
        self.assertTrue(cnmv.crypto_config.private_key_hardening)
        
        # Check Patterns
        pattern_ids = [p["id"] for p in self.state.architecture.enterprise_patterns]
        self.assertIn("crypto_cold_storage_hsm", pattern_ids)
        self.assertIn("market_abuse_monitoring", pattern_ids)

    def test_cnmv_audit_evidence(self):
        """Verify that CNMV evidence is correctly populated in the technical audit."""
        self.state.raw_input = {
            "business_type": "ROBOADVISOR",
            "target_retail_customers": True
        }
        self.engine.run_layer_2()
        
        audit_controls = [item["control"] for item in self.state.technical_audit]
        self.assertIn("CNMV Supervision", audit_controls)
        self.assertIn("Investor Protection", audit_controls)
        self.assertIn("Market Integrity", audit_controls)

if __name__ == "__main__":
    unittest.main()
