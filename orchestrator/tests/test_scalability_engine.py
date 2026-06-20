import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestScalabilityEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_proactive_scaling(self):
        """Verify that highly predicted traffic triggers proactive cloud plans."""
        self.state.scalability_profile.predicted_traffic_percent = 95.0
        self.state.scalability_profile.queue_length_critical = True
        
        # root -> high_predictive_traffic -> recommend_proactive_scaling
        self.engine.run_layer_2()
        
        scalability = self.engine.state.architecture.scalability
        self.assertEqual(scalability["strategy"], "Proactive Scaling Plan (Auto-Scaling / Reservations)")
        self.assertEqual(scalability["tier"], "recommend_proactive_scaling")

    def test_queue_saturation(self):
        """Verify that dangerous queue lengths trigger Bulkhead patterns."""
        self.state.scalability_profile.predicted_traffic_percent = 85.0
        self.state.scalability_profile.queue_length_critical = True
        
        # root -> queue_saturation -> recommend_bulkhead_pattern
        self.engine.run_layer_2()
        
        scalability = self.engine.state.architecture.scalability
        self.assertEqual(scalability["strategy"], "Bulkhead & Throttling Mitigation")
        self.assertEqual(scalability["tier"], "recommend_bulkhead_pattern")

    def test_cpu_io_saturation(self):
        """Verify that hardware utilization triggers physical scaling."""
        self.state.scalability_profile.predicted_traffic_percent = 80.0
        self.state.scalability_profile.queue_length_critical = False
        self.state.scalability_profile.cpu_io_saturation_percent = 85.0
        
        # root -> cpu_io_saturation -> recommend_vertical_horizontal
        self.engine.run_layer_2()
        
        scalability = self.engine.state.architecture.scalability
        self.assertEqual(scalability["strategy"], "Elastic Horizontal/Vertical Scaling")
        self.assertEqual(scalability["tier"], "recommend_vertical_horizontal")

    def test_latency_slas(self):
        """Verify that p99 SLA breaches trigger architectural CQRS interventions."""
        self.state.scalability_profile.predicted_traffic_percent = 75.0
        self.state.scalability_profile.cpu_io_saturation_percent = 60.0
        self.state.scalability_profile.latency_p99_violates_sla = True
        
        # root -> latency_breach -> recommend_cqrs_caching
        self.engine.run_layer_2()
        
        scalability = self.engine.state.architecture.scalability
        self.assertEqual(scalability["strategy"], "CQRS & Multi-Level Caching")
        self.assertEqual(scalability["tier"], "recommend_cqrs_caching")

    def test_healthy_monitoring(self):
        """Verify that low utilization maintains standard monitoring paths."""
        self.state.scalability_profile.predicted_traffic_percent = 60.0
        self.state.scalability_profile.queue_length_critical = False
        self.state.scalability_profile.cpu_io_saturation_percent = 40.0
        self.state.scalability_profile.latency_p99_violates_sla = False
        self.state.scalability_profile.traffic_saturation_percent = 50.0
        
        # root -> healthy_metrics -> recommend_continuous_monitoring
        self.engine.run_layer_2()
        
        scalability = self.engine.state.architecture.scalability
        self.assertEqual(scalability["strategy"], "Continuous Base Monitoring")
        self.assertEqual(scalability["tier"], "recommend_continuous_monitoring")

if __name__ == "__main__":
    unittest.main()
