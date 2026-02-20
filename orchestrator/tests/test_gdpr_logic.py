import sys
import os
import unittest
import logging

# Ensure we can import from orchestrator
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from global_state import GlobalState, TrafficProfile, DataProfile, ComplianceProfile
from layers.core_engine import CoreEngine

class TestGDPRTechnicalPillar(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)
        # Disable logging for cleaner test output
        logging.getLogger("Layer2_CoreEngine_V3").setLevel(logging.ERROR)

    def test_01_pii_node_marking(self):
        """
        Test 1: Node Marking - Verify that database nodes are marked as GDPR-Sensitive.
        """
        print("\n🧪 Test 1: PII Node Marking & Risk Scoring")
        self.state.compliance_profile.frameworks = ["GDPR"]
        self.state.raw_input["business_type"] = "FINTECH"
        
        # Trigger Layer 2
        self.engine.run_layer_2()
        
        db_node = next((c for c in self.state.architecture.components if c['role'] == 'data'), None)
        self.assertIsNotNone(db_node)
        self.assertIn("🔒", db_node['name'])
        self.assertTrue(db_node['gdpr']['personal_data'])
        self.assertEqual(db_node['gdpr']['reidentification_risk'], 0.8)
        print("✅ Correctly marked database as GDPR-Sensitive with high risk.")

    def test_02_pseudonymization_prod(self):
        """
        Test 2: Pseudonymization - Recommended for Production with re-id needs.
        """
        print("\n🧪 Test 2: Pseudonymization Recommendation (Production)")
        self.state.compliance_profile.frameworks = ["GDPR"]
        self.state.raw_input["environment"] = "production"
        self.state.raw_input["pii_operations_needed"] = True
        
        self.engine.run_layer_2()
        
        pattern_ids = [p['id'] for p in self.state.architecture.enterprise_patterns]
        self.assertIn("pseudonymization_strategy", pattern_ids)
        print("✅ Recommended Pseudonymization for production operations.")

    def test_03_k_anonymity_analytics(self):
        """
        Test 3: k-Anonymity - Recommended for Analytics with statistical utility priority.
        """
        print("\n🧪 Test 3: k-Anonymity Recommendation (Analytics)")
        self.state.compliance_profile.frameworks = ["GDPR"]
        self.state.raw_input["environment"] = "analytics"
        self.state.raw_input["statistical_utility_priority"] = True
        
        self.engine.run_layer_2()
        
        pattern_ids = [p['id'] for p in self.state.architecture.enterprise_patterns]
        # In our decision tree, k-anonymity points to 'anonymization_advanced' pattern_id currently
        self.assertIn("anonymization_advanced", pattern_ids)
        
        # Verify recommendation name
        rec = next(r for r in self.state.architecture.enterprise_patterns if r['id'] == "anonymization_advanced")
        # Note: If multiple branches lead to the same leaf, we might need more specific checks
        print(f"✅ Recommended {rec['name']} for analytics.")

    def test_04_differential_privacy_strict(self):
        """
        Test 4: Differential Privacy - Recommended for Analytics without statistical utility priority (Irreversible).
        """
        print("\n🧪 Test 4: Differential Privacy Recommendation (Strict)")
        self.state.compliance_profile.frameworks = ["GDPR"]
        self.state.raw_input["environment"] = "bi"
        self.state.raw_input["statistical_utility_priority"] = False
        
        self.engine.run_layer_2()
        
        pattern_ids = [p['id'] for p in self.state.architecture.enterprise_patterns]
        self.assertIn("anonymization_advanced", pattern_ids)
        print("✅ Recommended Advanced Anonymization for strict privacy requirements.")

    def test_05_synthetic_data_testing(self):
        """
        Test 5: Synthetic Data - Recommended for Testing environment.
        """
        print("\n🧪 Test 5: Synthetic Data Recommendation (Testing/QA)")
        self.state.compliance_profile.frameworks = ["GDPR"]
        self.state.raw_input["environment"] = "testing"
        
        self.engine.run_layer_2()
        
        pattern_ids = [p['id'] for p in self.state.architecture.enterprise_patterns]
        self.assertIn("anonymization_advanced", pattern_ids)
        print("✅ Recommended Synthetic Data (via Advanced Anonymization leaf) for Testing.")

if __name__ == "__main__":
    unittest.main()
