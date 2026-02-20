import unittest
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Set PYTHONPATH to include orchestrator
os.environ["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + ":" + os.environ.get("PYTHONPATH", "")

from orchestrator.global_state import GlobalState
from orchestrator.layers.core_engine import CoreEngine

class TestComplianceAudit(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_fintech_audit_ready_score(self):
        """Verify high compliance and audit score for Fintech with strict governance."""
        self.state.raw_input = {
            "business_type": "FINTECH",
            "destination_country": "US",
            "pii_operations_needed": True,
            "tags": ["AI"]
        }
        self.state.compliance_profile.frameworks = ["GDPR", "DORA"]
        
        self.engine.run_layer_2()
        
        # Verify scores
        self.assertGreaterEqual(self.state.compliance_score, 80)
        self.assertGreaterEqual(self.state.audit_ready_score, 70)
        
        # Verify evidence vault
        self.assertTrue(self.state.evidence_vault.immutable_logs_enabled)
        self.assertTrue(self.state.evidence_vault.data_registry_updated)
        self.assertEqual(self.state.evidence_vault.dpo_review_status, "Reviewed")
        
        # Verify technical audit report contains "Immutable"
        audit_controls = [item["control"] for item in self.state.technical_audit]
        self.assertIn("Audit Trails", audit_controls)
        
        # Verify pattern injection
        pattern_ids = [p["id"] for p in self.state.architecture.enterprise_patterns]
        self.assertIn("immutable_audit_logging", pattern_ids)

    def test_startup_low_governance_score(self):
        """Verify lower audit score for a low-risk startup without immutable logs."""
        self.state.raw_input = {
            "business_type": "STARTUP",
            "destination_country": "EU",
            "pii_operations_needed": False
        }
        self.state.compliance_profile.frameworks = []
        
        self.engine.run_layer_2()
        
        # Without GDPR/Strict governance, scores should be different (or defaults)
        # Note: In our current engine, non-GDPR critical might have empty score components
        # falling back to a default high score or 50.
        # But specifically, immutable_logs_enabled will be False
        self.assertFalse(self.state.evidence_vault.immutable_logs_enabled)
        # audit_ready_score should be lower than compliance_score by factor 0.6
        self.assertAlmostEqual(self.state.audit_ready_score, self.state.compliance_score * 0.6)

if __name__ == "__main__":
    unittest.main()
