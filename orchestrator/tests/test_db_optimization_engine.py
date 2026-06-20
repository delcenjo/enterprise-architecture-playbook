import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestDbOptimizationEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_fintech_reporting_composite_index(self):
        """Verify that a latency-critical fintech app gets composite indexing for reporting."""
        self.state.raw_input = {
            "business_type": "FINTECH_HA",
        }
        self.state.requirements = {"latency": "<20ms", "services": ["reporting"]} # latency_critical=True
        
        self.engine.run_layer_2()
        
        dbopt = self.engine.state.architecture.db_optimization
        self.assertEqual(dbopt["strategy"], "Composite & Covering Index Optimization")
        self.assertEqual(dbopt["tier"], "recommend_composite_indexing")

    def test_saas_high_concurrency_pooling(self):
        """Verify that a high-traffic system (without latency criticality) gets connection pooling."""
        self.state.raw_input = {
            "business_type": "SAAS_STANDARD",
        }
        self.state.traffic_profile.concurrent_users = 10000 
        self.state.requirements = {} # not latency critical
        
        self.engine.run_layer_2()
        
        dbopt = self.engine.state.architecture.db_optimization
        self.assertEqual(dbopt["strategy"], "Connection Pooling & PgBouncer/Proxy")
        self.assertEqual(dbopt["tier"], "recommend_pooling")

    def test_complex_transactional_locks(self):
        """Verify that a highly regulated / transactional bde system gets lock reviews."""
        self.state.raw_input = {
            "business_type": "ENTERPRISE_CORE",
            "is_bde_supervised": True
        }
        self.state.traffic_profile.concurrent_users = 1000 # below 5000 to bypass pool check; not latency_critical
        
        self.engine.run_layer_2()
        
        dbopt = self.engine.state.architecture.db_optimization
        self.assertEqual(dbopt["strategy"], "Transaction & Lock Review")
        self.assertEqual(dbopt["tier"], "recommend_lock_review")

if __name__ == "__main__":
    unittest.main()
