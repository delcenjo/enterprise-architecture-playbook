import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestPerformanceEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_fintech_spike_stress(self):
        """Verify that a regulated fintech gets Spike & Stress testing."""
        self.state.raw_input = {
            "business_type": "FINTECH_HA",
            "is_bde_supervised": True
        }
        self.state.traffic_profile.concurrent_users = 100000

        self.engine.run_layer_2()
        
        perf = self.engine.state.architecture.performance
        self.assertEqual(perf["strategy"], "Spike & Stress Testing (Gatling/k6)")
        self.assertEqual(perf["tier"], "recommend_spike_stress")
        self.assertIn("Spike Test", perf["pillars"])

    def test_saas_ci_cd_k6(self):
        """Verify that a standard SaaS (non-large scale) gets k6 CI/CD load testing."""
        self.state.raw_input = {
            "business_type": "SAAS_STANDARD",
        }
        self.state.traffic_profile.concurrent_users = 500

        self.engine.run_layer_2()
        
        perf = self.engine.state.architecture.performance
        self.assertEqual(perf["strategy"], "CI/CD Integrated Load Testing (k6)")
        self.assertEqual(perf["tier"], "recommend_k6_load")

    def test_microservices_soak(self):
        """Verify that a high-scale microservices architecture gets Soak Testing."""
        self.state.raw_input = {
            "business_type": "ENTERPRISE_CORE",
        }
        self.state.traffic_profile.concurrent_users = 100000
        self.state.requirements = {"services": ["auth", "orders"]}

        self.engine.run_layer_2()
        
        perf = self.engine.state.architecture.performance
        self.assertEqual(perf["strategy"], "Longevity/Soak Testing")
        self.assertEqual(perf["tier"], "recommend_soak_test")

if __name__ == "__main__":
    unittest.main()
