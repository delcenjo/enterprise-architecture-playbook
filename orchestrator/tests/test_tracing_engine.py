import unittest
import os
import sys
from typing import Dict, List, Any

from global_state import GlobalState, ArchitectureSpec
from layers.core_engine import CoreEngine

class TestTracingEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_distributed_fintech_tracing(self):
        """Verify that a complex fintech system gets Tail-based sampling."""
        self.state.raw_input = {
            "business_type": "FINTECH_HA",
            "payment_operations_enabled": True,
            "is_bde_supervised": True
        }
        self.state.requirements = {"services": ["auth", "payment", "ledger"]}
        
        self.engine.run_layer_2()
        
        tracing = self.engine.state.architecture.tracing
        self.assertEqual(tracing["strategy"], "Tail-based Sampling")
        self.assertEqual(tracing["tier"], "recommend_tail_based_tracing_full")
        self.assertIn("Traces", tracing["recommended_pillars"])

    def test_startup_monolith_tracing(self):
        """Verify that a small monolith doesn't get advanced tracing."""
        self.state.raw_input = {
            "business_type": "STARTUP_MVP"
        }
        self.state.requirements = {"services": ["api"]}
        
        self.engine.run_layer_2()
        
        tracing = self.engine.state.architecture.tracing
        self.assertEqual(tracing["strategy"], "Minimal/None")
        self.assertNotIn("Traces", tracing["recommended_pillars"])

    def test_high_load_standard_tracing(self):
        """Verify that high load triggers head-based sampling."""
        self.state.raw_input = {
            "business_type": "MARKETPLACE",
        }
        self.state.traffic_profile.requests_per_second = 5000
        self.state.traffic_profile.concurrent_users = 100000
        self.state.requirements = {"services": ["frontend", "catalog", "order"]}
        
        self.engine.run_layer_2()
        
        tracing = self.engine.state.architecture.tracing
        self.assertEqual(tracing["strategy"], "Head-based Sampling")
        self.assertEqual(tracing["tier"], "recommend_head_based_tracing_lean")

if __name__ == "__main__":
    unittest.main()
