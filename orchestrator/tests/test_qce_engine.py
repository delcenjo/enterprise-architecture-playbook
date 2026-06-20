import unittest
import json
import os
import sys

# Ensure orchestrator is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestQCEEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_mica_aml_qce_flow(self):
        """Verify that a crypto startup triggers QCE MiCA/AML logic."""
        self.state.raw_input = {
            "business_type": "CRYPTO_EXCHANGE",
            "custody_enabled": True, # Triggers MiCA
            "remote_onboarding_enabled": True, # Triggers AML High Risk
            "aml_geography_risk": 4, # High
            "aml_activity_risk": 4,
            "aml_product_risk": 4
        }
        self.engine.run_layer_2()

        self.assertGreater(self.state.compliance_score, 0)

        audit_controls = [item["control"] for item in self.state.technical_audit]
        self.assertIn("Unified Regulatory Compliance (QCE)", audit_controls)
        self.assertIn("QCE Mandate", audit_controls)

        qce_evidence = next(item for item in self.state.technical_audit if item["control"] == "Unified Regulatory Compliance (QCE)")
        self.assertIn("MiCA_CASP", qce_evidence["evidence"])
        self.assertIn("AML_LEY_10_2010", qce_evidence["evidence"])

    def test_psd2_mifid_qce_flow(self):
        """Verify that a Roboadvisor with payments triggers MiFID/PSD2 logic."""
        self.state.raw_input = {
            "business_type": "ROBOADVISOR",
            "payment_operations_enabled": True, # Triggers PSD2
            "target_retail_customers": True # Triggers MiFID
        }
        self.engine.run_layer_2()
        
        qce_evidence = next(item for item in self.state.technical_audit if item["control"] == "Unified Regulatory Compliance (QCE)")
        self.assertIn("GDPR_EU", qce_evidence["evidence"])
        self.assertIn("AML_LEY_10_2010", qce_evidence["evidence"])

    def test_qce_score_adjustment(self):
        """Verify that a compliance score is generated for a crypto exchange with custody."""
        self.state.raw_input = {
            "business_type": "CRYPTO_EXCHANGE",
            "custody_enabled": True
        }
        self.engine.run_layer_2()
        self.assertTrue(0 < self.state.compliance_score <= 100)

if __name__ == "__main__":
    unittest.main()
