import unittest
import json
import os
import sys

# Ensure orchestrator is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from global_state import GlobalState, TrafficProfile, DataProfile, ComplianceProfile
from layers.core_engine import CoreEngine

class TestPSD2SCA(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_psd2_sca_mandatory(self):
        """Verify that SCA is mandatory for high-value transactions in supervised entities."""
        self.state.raw_input = {
            "business_type": "FINTECH_PAYMENTS",
            "payment_operations_enabled": True,
            "avg_transaction_value": 150,
            "historical_fraud_rate": 0.05, # High fraud, no TRA possible
            "pii_operations_needed": True
        }
        self.engine.run_layer_2()

        
        psd2 = self.state.psd2_compliance
        self.assertTrue(psd2.sca_required)
        self.assertEqual(psd2.exemption_applied, "None")
        self.assertTrue(psd2.sca_config.dynamic_linking_active)
        self.assertIn("Possession", psd2.sca_config.factors_enabled)
        
        audit_controls = [item["control"] for item in self.state.technical_audit]
        self.assertIn("PSD2/SCA", audit_controls)
        self.assertIn("Dynamic Linking", audit_controls)
        
        pattern_ids = [p["id"] for p in self.state.architecture.enterprise_patterns]
        self.assertIn("sca_multi_factor", pattern_ids)
        self.assertIn("dynamic_linking_vault", pattern_ids)

    def test_psd2_low_value_exemption(self):
        """Verify Low Value exemption for transactions < 30€."""
        self.state.raw_input = {
            "business_type": "PAYMENT_GATEWAY",
            "payment_operations_enabled": True,
            "avg_transaction_value": 25,
            "historical_fraud_rate": 0.01,
            "pii_operations_needed": False
        }
        self.engine.run_layer_2()
        
        psd2 = self.state.psd2_compliance
        self.assertFalse(psd2.sca_required)
        self.assertEqual(psd2.exemption_applied, "Low Value")
        
        audit_controls = [item["control"] for item in self.state.technical_audit]
        self.assertIn("SCA Exemption", audit_controls)

    def test_psd2_tra_exemption(self):
        """Verify TRA exemption for transactions with low fraud rate."""
        self.state.raw_input = {
            "business_type": "FINTECH",
            "payment_operations_enabled": True,
            "avg_transaction_value": 80,
            "historical_fraud_rate": 0.05,
            "pii_operations_needed": True
        }
        self.engine.run_layer_2()

        psd2 = self.state.psd2_compliance
        self.assertTrue(psd2.sca_required)
        self.assertEqual(psd2.exemption_applied, "TRA")
        
        pattern_ids = [p["id"] for p in self.state.architecture.enterprise_patterns]
        self.assertIn("tra_risk_engine", pattern_ids)

    def test_psd2_non_scope(self):
        """Verify non-payment entities don't trigger PSD2 logic."""
        self.state.raw_input = {
            "business_type": "E-COMMERCE_LOGISTICS",
            "payment_operations_enabled": False
        }
        self.engine.run_layer_2()
        
        self.assertFalse(self.state.psd2_compliance.sca_required)
        self.assertEqual(self.state.psd2_compliance.exemption_applied, "None")

if __name__ == "__main__":
    unittest.main()
