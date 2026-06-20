import unittest
import json
import os
import sys

# Ensure orchestrator is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestObservabilityEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_distributed_microservices_observability(self):
        """Verify that a distributed microservices system recommends all pillars."""
        self.state.raw_input = {
            "business_type": "FINTECH_HA"
        }
        # Mock components to trigger is_microservices
        self.state.requirements = {
            "functional": {
                "components": ["auth", "payments", "ledger", "notification"]
            }
        }
        
        self.engine.run_layer_2()
        
        obs = self.engine.state.architecture.observability
        self.assertIn("Traces", obs["pillars"])
        self.assertIn("Metrics", obs["pillars"])
        self.assertIn("Logs", obs["pillars"])
        self.assertEqual(obs["recommendation_id"], "recommend_metrics_logs_traces")
        self.assertIn("Jaeger", obs["tools"])
        self.assertIn("Prometheus", obs["tools"])

    def test_critical_system_full_stack(self):
        """Verify that high criticality (e.g. PSD2) triggers all pillars."""
        self.state.raw_input = {
            "business_type": "FINTECH_HA",
            "payment_operations_enabled": True
        }
        
        self.engine.run_layer_2()
        
        obs = self.engine.state.architecture.observability
        self.assertEqual(obs["recommendation_id"], "recommend_all_pillars")
        self.assertIn("Alertas proactivas", obs["features"])

    def test_regulatory_logging_gdpr(self):
        """Verify that GDPR/AML mandates centralized logging."""
        self.state.raw_input = {
            "business_type": "SAAS_STANDARD",
            "is_gdpr_critical": True
        }
        # Ensure it's NOT distributed to avoid Traces leaf taking precedence
        self.state.requirements = {
            "functional": {
                "components": ["monolith"]
            }
        }
        
        self.engine.run_layer_2()
        
        obs = self.engine.state.architecture.observability
        self.assertIn("Logs", obs["pillars"])
        self.assertIn("Secure log retention", obs["features"])

if __name__ == "__main__":
    unittest.main()
