import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestOKREngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_reliability_focus(self):
        """Verify that high failure rate triggers Reliability MTTR prioritization."""
        self.state.okr_profile.change_failure_rate_high = True # Top priority
        self.state.okr_profile.deployment_frequency_low = True 
        
        # root -> high_failure_rate_or_mttr -> recommend_reliability_focus
        self.engine.run_layer_2()
        
        okrs = self.engine.state.architecture.okrs
        self.assertEqual(okrs["strategy"], "Reliability & Resilience OKRs")
        self.assertEqual(okrs["tier"], "recommend_reliability_focus")

    def test_speed_focus(self):
        """Verify that low delivery speed triggers Delivery Speed focus."""
        self.state.okr_profile.change_failure_rate_high = False
        self.state.okr_profile.deployment_frequency_low = True # Triggers speed constraint
        
        # root -> low_deployment_frequency -> recommend_speed_focus
        self.engine.run_layer_2()
        
        okrs = self.engine.state.architecture.okrs
        self.assertEqual(okrs["strategy"], "Delivery Speed & Flow OKRs")
        self.assertEqual(okrs["tier"], "recommend_speed_focus")

    def test_strategic_alignment(self):
        """Verify that business priorities route explicitly to mapped technical goals."""
        self.state.okr_profile.deployment_frequency_low = False 
        self.state.okr_profile.change_failure_rate_high = False
        self.state.okr_profile.strategic_business_goal_active = True # Triggers strategy
        
        # root -> strategic_business_goal -> recommend_strategic_alignment
        self.engine.run_layer_2()
        
        okrs = self.engine.state.architecture.okrs
        self.assertEqual(okrs["strategy"], "Strategic Business Alignment OKRs")
        self.assertEqual(okrs["tier"], "recommend_strategic_alignment")

    def test_quality_degradation(self):
        """Verify that falling coverage routes to Code Quality refactoring OKRs."""
        self.state.okr_profile.strategic_business_goal_active = False
        self.state.okr_profile.quality_degradation = True # Triggers quality metrics
        
        # root -> quality_degradation -> recommend_quality_focus
        self.engine.run_layer_2()
        
        okrs = self.engine.state.architecture.okrs
        self.assertEqual(okrs["strategy"], "Code Quality & Debt Reduction OKRs")
        self.assertEqual(okrs["tier"], "recommend_quality_focus")

    def test_operational_maintenance(self):
        """Verify that healthy DORA metrics fallback to steady state tracking."""
        self.state.okr_profile.change_failure_rate_high = False
        self.state.okr_profile.deployment_frequency_low = False 
        self.state.okr_profile.strategic_business_goal_active = False
        self.state.okr_profile.quality_degradation = False
        
        # root -> stable_metrics -> recommend_operational_maintenance
        self.engine.run_layer_2()
        
        okrs = self.engine.state.architecture.okrs
        self.assertEqual(okrs["strategy"], "Operational Consistency OKRs")
        self.assertEqual(okrs["tier"], "recommend_operational_maintenance")

if __name__ == "__main__":
    unittest.main()
