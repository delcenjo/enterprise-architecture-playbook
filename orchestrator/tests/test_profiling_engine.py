import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestProfilingEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_fintech_lightweight_cpu(self):
        """Verify that a regulated HA system gets production-safe lightweight profiling."""
        self.state.raw_input = {
            "business_type": "FINTECH_HA",
            "is_bde_supervised": True
        }
        self.state.requirements = {"latency": "<50ms"}

        self.engine.run_layer_2()
        
        prof = self.engine.state.architecture.profiling
        self.assertEqual(prof["strategy"], "Lightweight Sampling Profiling (Continuous)")
        self.assertEqual(prof["tier"], "recommend_lightweight_cpu")
        self.assertIn("FlameGraphs", prof["pillars"])

    def test_startup_deep_cpu(self):
        """Verify that a non-regulated fast startup gets deep CPU profiling."""
        self.state.raw_input = {
            "business_type": "STARTUP_MVP",
        }
        self.state.requirements = {"latency": "<100ms", "services": ["api"]}

        self.engine.run_layer_2()
        
        prof = self.engine.state.architecture.profiling
        self.assertEqual(prof["strategy"], "Deep CPU Profiling (FlameGraphs)")
        self.assertEqual(prof["tier"], "recommend_deep_cpu")

    def test_high_scale_memory(self):
        """Verify that a very high scale system gets memory profiling."""
        self.state.raw_input = {
            "business_type": "SAAS_STANDARD",
        }
        self.state.traffic_profile.concurrent_users = 50000

        self.engine.run_layer_2()
        
        prof = self.engine.state.architecture.profiling
        self.assertEqual(prof["strategy"], "Memory Profiling & Heap Analysis")
        self.assertEqual(prof["tier"], "recommend_memory_profiling")

if __name__ == "__main__":
    unittest.main()
