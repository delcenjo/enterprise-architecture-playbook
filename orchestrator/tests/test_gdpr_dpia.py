import unittest
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from orchestrator.global_state import GlobalState, DataProfile, ComplianceProfile, TrafficProfile
from orchestrator.layers.core_engine import CoreEngine

class TestGDPRDPIA(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_dpia_trigger_high_risk_fintech(self):
        """Verify DPIA is mandatory for Fintech with Large Scale processing."""
        self.state.raw_input = {
            "business_type": "FINTECH",
            "pii_operations_needed": True,
            "tags": ["AI", "scoring"]
        }
        self.state.traffic_profile.concurrent_users = 60000
        self.state.compliance_profile.frameworks = ["GDPR"]
        
        self.engine.run_layer_2()
        
        report = self.state.architecture.dpia_report
        self.assertTrue(report.is_mandatory)
        self.assertIn("Large scale processing", report.triggers)
        self.assertIn("Automated decision making with legal effects", report.triggers)
        self.assertEqual(report.overall_risk_level, "Extreme")
        self.assertTrue(report.dpo_approval_required)

        
        # Verify specific risks
        risk_descriptions = [r.description for r in report.risks]
        self.assertTrue(any("Discriminación algorítmica" in d for d in risk_descriptions))

    def test_dpia_not_mandatory_startup(self):
        """Verify DPIA is not mandatory for a lean startup with non-sensitive data."""
        self.state.raw_input = {
            "business_type": "SAAS",
            "pii_operations_needed": False
        }
        self.state.traffic_profile.concurrent_users = 100
        self.state.compliance_profile.frameworks = ["None"]
        
        self.engine.run_layer_2()
        
        report = self.state.architecture.dpia_report
        self.assertFalse(report.is_mandatory)
        self.assertEqual(report.overall_risk_level, "Low")

    def test_algorithmic_impact_recommendation(self):
        """Verify that automated decisions trigger Algorithmic Impact Assessment pattern."""
        self.state.raw_input = {
            "business_type": "FINTECH",
            "pii_operations_needed": True
        }
        self.state.compliance_profile.frameworks = ["GDPR"]
        
        self.engine.run_layer_2()
        
        pattern_ids = [p["id"] for p in self.state.architecture.enterprise_patterns]
        self.assertIn("algorithmic_impact_assessment", pattern_ids)

if __name__ == "__main__":
    unittest.main()
