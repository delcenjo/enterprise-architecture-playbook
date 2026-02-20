import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestSeniorEvalEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_strong_senior_hire(self):
        """Verify routing for a score >= 4.5."""
        self.state.senior_eval_profile.sys_design_score = 4.8 # 1.68
        self.state.senior_eval_profile.coding_score = 4.5 # 0.90
        self.state.senior_eval_profile.tradeoff_score = 4.8 # 0.72
        self.state.senior_eval_profile.behavioral_score = 5.0 # 0.75
        self.state.senior_eval_profile.comm_score = 4.5 # 0.45
        self.state.senior_eval_profile.product_score = 4.0 # 0.20
        # Total: 4.70 -> Strong Hire
        
        self.engine.run_layer_2()
        senior = self.engine.state.architecture.senior_evaluation
        self.assertEqual(senior["tier"], "recommend_strong_senior")
        self.assertGreaterEqual(senior["calculated_score"], 4.5)

    def test_solid_senior_hire(self):
        """Verify routing for a score between 3.8 and 4.49."""
        self.state.senior_eval_profile.sys_design_score = 4.0 # 1.40
        self.state.senior_eval_profile.coding_score = 4.0 # 0.80
        self.state.senior_eval_profile.tradeoff_score = 4.0 # 0.60
        self.state.senior_eval_profile.behavioral_score = 4.0 # 0.60
        self.state.senior_eval_profile.comm_score = 4.0 # 0.40
        self.state.senior_eval_profile.product_score = 4.0 # 0.20
        # Total: 4.0 -> Solid Hire
        
        self.engine.run_layer_2()
        senior = self.engine.state.architecture.senior_evaluation
        self.assertEqual(senior["tier"], "recommend_solid_senior")
        self.assertGreaterEqual(senior["calculated_score"], 3.8)
        self.assertLess(senior["calculated_score"], 4.5)

    def test_false_senior(self):
        """Verify routing for a candidate high in coding but low in design/behavior (Mid+ disguised)."""
        self.state.senior_eval_profile.sys_design_score = 2.5 # 0.875
        self.state.senior_eval_profile.coding_score = 4.8 # 0.96
        self.state.senior_eval_profile.tradeoff_score = 2.0 # 0.30
        self.state.senior_eval_profile.behavioral_score = 3.0 # 0.45
        self.state.senior_eval_profile.comm_score = 3.5 # 0.35
        self.state.senior_eval_profile.product_score = 3.0 # 0.15
        # Total: 3.085 -> Reject (Mid+ Disguised / Reject)
        
        self.engine.run_layer_2()
        senior = self.engine.state.architecture.senior_evaluation
        self.assertEqual(senior["tier"], "recommend_reject")
        self.assertLess(senior["calculated_score"], 3.2)

    def test_mid_plus_disguised(self):
        """Verify routing for a candidate between 3.2 and 3.79."""
        self.state.senior_eval_profile.sys_design_score = 3.0 # 1.05
        self.state.senior_eval_profile.coding_score = 4.5 # 0.90
        self.state.senior_eval_profile.tradeoff_score = 3.0 # 0.45
        self.state.senior_eval_profile.behavioral_score = 3.5 # 0.525
        self.state.senior_eval_profile.comm_score = 4.0 # 0.40
        self.state.senior_eval_profile.product_score = 3.0 # 0.15
        # Total: 3.475 -> Mid+
        
        self.engine.run_layer_2()
        senior = self.engine.state.architecture.senior_evaluation
        self.assertEqual(senior["tier"], "recommend_mid_disguised")
        self.assertGreaterEqual(senior["calculated_score"], 3.2)
        self.assertLess(senior["calculated_score"], 3.8)

if __name__ == "__main__":
    unittest.main()
