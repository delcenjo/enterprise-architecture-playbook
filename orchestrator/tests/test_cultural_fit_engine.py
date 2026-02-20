import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestCulturalFitEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_cultural_multiplier(self):
        """Verify routing for a score >= 4.5."""
        self.state.cultural_fit_profile.ownership_score = 5.0 # 1.25
        self.state.cultural_fit_profile.conflict_score = 4.8 # 0.96
        self.state.cultural_fit_profile.feedback_score = 4.5 # 0.90
        self.state.cultural_fit_profile.collaboration_score = 4.5 # 0.675
        self.state.cultural_fit_profile.transparency_score = 4.8 # 0.48
        self.state.cultural_fit_profile.learning_score = 4.2 # 0.42
        # Total: 4.685 -> Multiplier
        
        self.engine.run_layer_2()
        culture = self.engine.state.architecture.cultural_fit
        self.assertEqual(culture["tier"], "recommend_cultural_multiplier")
        self.assertGreaterEqual(culture["calculated_score"], 4.5)

    def test_solid_cultural_fit(self):
        """Verify routing for a score between 4.0 and 4.49."""
        self.state.cultural_fit_profile.ownership_score = 4.0 # 1.00
        self.state.cultural_fit_profile.conflict_score = 4.0 # 0.80
        self.state.cultural_fit_profile.feedback_score = 4.0 # 0.80
        self.state.cultural_fit_profile.collaboration_score = 4.0 # 0.60
        self.state.cultural_fit_profile.transparency_score = 4.0 # 0.40
        self.state.cultural_fit_profile.learning_score = 4.0 # 0.40
        # Total: 4.0 -> Solid
        
        self.engine.run_layer_2()
        culture = self.engine.state.architecture.cultural_fit
        self.assertEqual(culture["tier"], "recommend_solid_fit")
        self.assertGreaterEqual(culture["calculated_score"], 4.0)
        self.assertLess(culture["calculated_score"], 4.5)

    def test_moderate_friction_risk(self):
        """Verify routing for a candidate between 3.5 and 3.99."""
        self.state.cultural_fit_profile.ownership_score = 3.5 # 0.875
        self.state.cultural_fit_profile.conflict_score = 3.8 # 0.76
        self.state.cultural_fit_profile.feedback_score = 3.2 # 0.64
        self.state.cultural_fit_profile.collaboration_score = 4.0 # 0.60
        self.state.cultural_fit_profile.transparency_score = 3.8 # 0.38
        self.state.cultural_fit_profile.learning_score = 4.5 # 0.45
        # Total: 3.705 -> Moderate Risk
        
        self.engine.run_layer_2()
        culture = self.engine.state.architecture.cultural_fit
        self.assertEqual(culture["tier"], "recommend_moderate_risk")
        self.assertGreaterEqual(culture["calculated_score"], 3.5)
        self.assertLess(culture["calculated_score"], 4.0)

    def test_high_friction_toxic(self):
        """Verify routing for a candidate <3.5 (Toxic Rockstar)."""
        self.state.cultural_fit_profile.ownership_score = 2.5 # 0.625
        self.state.cultural_fit_profile.conflict_score = 2.0 # 0.40
        self.state.cultural_fit_profile.feedback_score = 1.5 # 0.30
        self.state.cultural_fit_profile.collaboration_score = 2.0 # 0.30
        self.state.cultural_fit_profile.transparency_score = 3.0 # 0.30
        self.state.cultural_fit_profile.learning_score = 4.5 # 0.45
        # Total: 2.375 -> High Friction / Reject
        
        self.engine.run_layer_2()
        culture = self.engine.state.architecture.cultural_fit
        self.assertEqual(culture["tier"], "recommend_high_friction_reject")
        self.assertLess(culture["calculated_score"], 3.5)

if __name__ == "__main__":
    unittest.main()
