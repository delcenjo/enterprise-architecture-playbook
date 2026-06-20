import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestTradeoffEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_intentional_tech_debt(self):
        """Verify that core business with massive time urgency accepts intentional tech debt."""
        self.state.tradeoff_profile.is_core_business = True
        self.state.tradeoff_profile.time_to_market_critical = True

        self.engine.run_layer_2()
        
        tradeoff = self.engine.state.architecture.tradeoff_analysis
        self.assertEqual(tradeoff["strategy"], "Accept Intentional Technical Debt (Optimize for Speed)")
        self.assertEqual(tradeoff["tier"], "recommend_intentional_tech_debt")

    def test_saas_buy(self):
        """Verify that non-core commodity functions route to mature SaaS acquisitions."""
        self.state.tradeoff_profile.is_core_business = False
        self.state.tradeoff_profile.mature_saas_available = True
        
        self.engine.run_layer_2()
        
        tradeoff = self.engine.state.architecture.tradeoff_analysis
        self.assertEqual(tradeoff["strategy"], "Buy / License SaaS Solution")
        self.assertEqual(tradeoff["tier"], "recommend_buy_saas")

    def test_internal_build(self):
        """Verify that core, long-term investments mandate robust internal execution."""
        self.state.tradeoff_profile.is_core_business = True
        self.state.tradeoff_profile.time_to_market_critical = False
        self.state.tradeoff_profile.long_term_maintenance_critical = True
        
        self.engine.run_layer_2()
        
        tradeoff = self.engine.state.architecture.tradeoff_analysis
        self.assertEqual(tradeoff["strategy"], "Execute Full Internal Build")
        self.assertEqual(tradeoff["tier"], "recommend_internal_build")

    def test_outsourcing(self):
        """Verify that non-core budget constrained items route to partial outsourcing."""
        self.state.tradeoff_profile.is_core_business = False
        self.state.tradeoff_profile.mature_saas_available = False
        self.state.tradeoff_profile.budget_constrained = True
        
        self.engine.run_layer_2()
        
        tradeoff = self.engine.state.architecture.tradeoff_analysis
        self.assertEqual(tradeoff["strategy"], "Strategic Outsourcing / Minimum Viable SaaS")
        self.assertEqual(tradeoff["tier"], "recommend_outsourcing_buy_minimum")

    def test_standard_evaluation(self):
        """Verify that balanced scenarios route to a standard TCO build/buy analysis matrix."""
        self.state.tradeoff_profile.is_core_business = True
        self.state.tradeoff_profile.time_to_market_critical = False
        self.state.tradeoff_profile.long_term_maintenance_critical = False
        self.state.tradeoff_profile.mature_saas_available = False
        self.state.tradeoff_profile.budget_constrained = False
        
        self.engine.run_layer_2()
        
        tradeoff = self.engine.state.architecture.tradeoff_analysis
        self.assertEqual(tradeoff["strategy"], "Standard Trade-off Matrix Evaluation")
        self.assertEqual(tradeoff["tier"], "recommend_standard_evaluation")

if __name__ == "__main__":
    unittest.main()
