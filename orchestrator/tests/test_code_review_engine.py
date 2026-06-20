import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestCodeReviewEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_missing_ci(self):
        """Verify that lacking CI tools forces a manual review + automation initiative."""
        self.state.code_review_profile.has_automated_ci = False # Triggers no_ci
        self.engine.run_layer_2()
        
        review = self.engine.state.architecture.code_review
        self.assertEqual(review["strategy"], "Strict Manual Review & CI Automation Plan")
        self.assertEqual(review["tier"], "recommend_manual_and_automate")

    def test_gates_failing(self):
        """Verify that failing quality gates (like low coverage in SonarQube) blocks the merge."""
        self.state.code_review_profile.has_automated_ci = True 
        self.state.code_review_profile.quality_gates_passing = False # Triggers gates_failing
        self.engine.run_layer_2()
        
        review = self.engine.state.architecture.code_review
        self.assertEqual(review["strategy"], "Block Merge (Resolve Quality Gates)")
        self.assertEqual(review["tier"], "recommend_block_merge")

    def test_critical_violations(self):
        """Verify that critical bugs/security issues trigger senior escalation."""
        self.state.code_review_profile.quality_gates_passing = True
        self.state.code_review_profile.critical_violations = 2 # Triggers critical_violations
        self.engine.run_layer_2()
        
        review = self.engine.state.architecture.code_review
        self.assertEqual(review["strategy"], "Senior Escalation & Security Audit")
        self.assertEqual(review["tier"], "recommend_escalate_senior")

    def test_massive_pr(self):
        """Verify that a 600 LOC PR gets rejected and split."""
        self.state.code_review_profile.quality_gates_passing = True 
        self.state.code_review_profile.critical_violations = 0
        self.state.code_review_profile.pr_size_loc = 650 # Triggers massive_pr
        self.engine.run_layer_2()
        
        review = self.engine.state.architecture.code_review
        self.assertEqual(review["strategy"], "PR Splitting & Parallel Review")
        self.assertEqual(review["tier"], "recommend_split_pr")

    def test_healthy_standard(self):
        """Verify that a normal sized PR passing gates gets the standard hybrid scalable recommendation."""
        self.state.code_review_profile.quality_gates_passing = True 
        self.state.code_review_profile.critical_violations = 0
        self.state.code_review_profile.pr_size_loc = 150 # Triggers passing_healthy
        self.state.code_review_profile.has_automated_ci = True
        self.engine.run_layer_2()
        
        review = self.engine.state.architecture.code_review
        self.assertEqual(review["strategy"], "Continuous Hybrid Review")
        self.assertEqual(review["tier"], "recommend_hybrid_scale")

if __name__ == "__main__":
    unittest.main()
