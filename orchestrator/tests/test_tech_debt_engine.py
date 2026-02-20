import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestTechDebtEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_critical_debt_high_business_impact(self):
        """Verify that terrible SQALE on a high traffic site escalates to the CTO."""
        self.state.tech_debt_profile.sqale_index = 3.5 # Triggers critical_debt
        self.state.traffic_profile.requests_per_second = 10000 # Triggers high business impact
        
        # root -> critical_debt -> business_impact_check -> yes -> recommend_immediate_refactor_cto
        self.engine.run_layer_2()
        
        debt = self.engine.state.architecture.tech_debt
        self.assertEqual(debt["strategy"], "Strategic Refactoring Freeze (Escalate to CTO)")
        self.assertEqual(debt["tier"], "recommend_immediate_refactor_cto")

    def test_critical_debt_sprint(self):
        """Verify that terrible Code Climate on a normal site triggers a dedicated sprint."""
        self.state.tech_debt_profile.code_climate = 1.0 # Triggers critical_debt
        self.state.traffic_profile.requests_per_second = 100 # Normal scale
        
        # root -> critical_debt -> business_impact_check -> no -> recommend_immediate_refactor_sprint
        self.engine.run_layer_2()
        
        debt = self.engine.state.architecture.tech_debt
        self.assertEqual(debt["strategy"], "Dedicated Tech Debt Sprint")
        self.assertEqual(debt["tier"], "recommend_immediate_refactor_sprint")

    def test_low_coverage(self):
        """Verify that failing coverage mandates a testing sprint."""
        self.state.tech_debt_profile.code_climate = 3.5 # OK
        self.state.tech_debt_profile.sqale_index = 8.0 # OK
        self.state.tech_debt_profile.test_coverage = 45.0 # Fails <60%
        
        # root -> low_coverage -> recommend_testing_sprint
        self.engine.run_layer_2()
        
        debt = self.engine.state.architecture.tech_debt
        self.assertEqual(debt["strategy"], "Automated Testing & Coverage Remediation")
        self.assertEqual(debt["tier"], "recommend_testing_sprint")

    def test_cyclomatic_complexity(self):
        """Verify that high complexity triggers domain splitting."""
        self.state.tech_debt_profile.test_coverage = 85.0 # OK
        self.state.tech_debt_profile.cyclomatic_complexity = 22 # Fails >15
        
        # root -> high_complexity -> recommend_module_split
        self.engine.run_layer_2()
        
        debt = self.engine.state.architecture.tech_debt
        self.assertEqual(debt["strategy"], "Domain/Module Splitting (Strangler Fig)")
        self.assertEqual(debt["tier"], "recommend_module_split")

    def test_manageable_debt(self):
        """Verify that good metrics trigger the standard Boy Scout rule."""
        self.state.tech_debt_profile.sqale_index = 9.0 
        self.state.tech_debt_profile.test_coverage = 85.0 
        self.state.tech_debt_profile.cyclomatic_complexity = 8
        self.state.tech_debt_profile.code_climate = 3.5
        
        # root -> manageable_debt -> recommend_incremental_refactor
        self.engine.run_layer_2()
        
        debt = self.engine.state.architecture.tech_debt
        self.assertEqual(debt["strategy"], "Incremental Boy-Scout Refactoring")
        self.assertEqual(debt["tier"], "recommend_incremental_refactor")

if __name__ == "__main__":
    unittest.main()
