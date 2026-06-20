import sys
import os
import unittest
import logging

# Ensure we can import from orchestrator
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from global_state import GlobalState, TrafficProfile, DataProfile, ComplianceProfile
from layers.core_engine import CoreEngine

class TestGDPRRetentionPillar(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)
        # Disable logging for cleaner test output
        logging.getLogger("Layer2_CoreEngine_V3").setLevel(logging.ERROR)

    def test_01_crypto_shredding_injection(self):
        """
        Test 1: Crypto-Shredding - Triggered by GDPR + Critical Sensitivity.
        """
        print("\nTest 1: Crypto-Shredding & KMS Injection")
        self.state.compliance_profile.frameworks = ["GDPR"]
        self.state.data_profile.sensitivity = "critical"
        self.state.raw_input["business_type"] = "FINTECH" # Should trigger deletion_proof -> crypto_shredding
        
        self.engine.run_layer_2()
        
        pattern_ids = [p['id'] for p in self.state.architecture.enterprise_patterns]
        self.assertIn("crypto_shredding", pattern_ids)
        
        # Verify KMS Cluster injection
        kms_node = next((c for c in self.state.architecture.components if "KMS" in c['name']), None)
        self.assertIsNotNone(kms_node)
        self.assertEqual(kms_node['type'], "KMS-HSM")
        
        # Verify Deletion Audit injection
        audit_node = next((c for c in self.state.architecture.components if "Deletion Proof" in c['name']), None)
        self.assertIsNotNone(audit_node)
        print("Correctly recommended Crypto-Shredding and injected security components.")

    def test_02_retention_conflict_resolution(self):
        """
        Test 2: Retention Conflict - FINTECH environment should show segmented policies.
        """
        print("\nTest 2: Retention Conflict (GDPR vs AML)")
        self.state.compliance_profile.frameworks = ["GDPR", "AML"] # Conflict trigger
        self.state.raw_input["business_type"] = "FINTECH"
        
        self.engine.run_layer_2()
        
        # Verify lifecycle policies
        policies = self.state.architecture.lifecycle.policies
        categories = [p.category for p in policies]
        self.assertIn("personal_data", categories)
        self.assertIn("aml_records", categories)
        
        # Verify segmented retention pattern
        pattern_ids = [p['id'] for p in self.state.architecture.enterprise_patterns]
        # In our tree, conflict check leads to recommend_gdpr_segmented_retention -> automated_ttl_enforcement id
        self.assertIn("automated_ttl_enforcement", pattern_ids)
        print("Successfully resolved retention conflicts with segmented policies.")

    def test_03_standard_ttl_enforcement(self):
        """
        Test 3: Standard TTL - Recommended for GDPR SaaS.
        """
        print("\nTest 3: Standard TTL Enforcement")
        self.state.compliance_profile.frameworks = ["GDPR"]
        self.state.raw_input["business_type"] = "SAAS"
        self.state.data_profile.sensitivity = "medium" # Not critical -> no shredding needed by default
        
        self.engine.run_layer_2()
        
        pattern_ids = [p['id'] for p in self.state.architecture.enterprise_patterns]
        self.assertIn("automated_ttl_enforcement", pattern_ids)
        self.assertNotIn("crypto_shredding", pattern_ids)
        print("Recommended standard TTL for non-critical SaaS environment.")

if __name__ == "__main__":
    unittest.main()
