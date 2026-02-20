import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestTPMEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_regulatory_blockers(self):
        """Verify that hard blockers suspend abstract feature ranking frameworks."""
        self.state.tpm_profile.has_regulatory_blockers = True # Top priority
        self.state.tpm_profile.has_financial_impact = True 
        
        # root -> regulatory_blockers -> recommend_blocker_resolution
        self.engine.run_layer_2()
        
        tpm = self.engine.state.architecture.tpm
        self.assertEqual(tpm["strategy"], "Halt & Resolve Hard Dependencies")
        self.assertEqual(tpm["tier"], "recommend_blocker_resolution")

    def test_resource_constrained(self):
        """Verify that tight bandwidth triggers Effort-weighted reprioritization."""
        self.state.tpm_profile.has_regulatory_blockers = False
        self.state.tpm_profile.resource_constrained = True # Triggers constraint
        
        # root -> resource_constrained -> recommend_effort_reprioritization
        self.engine.run_layer_2()
        
        tpm = self.engine.state.architecture.tpm
        self.assertEqual(tpm["strategy"], "Aggressive Resource Constraint Adjustment")
        self.assertEqual(tpm["tier"], "recommend_effort_reprioritization")

    def test_kano_model(self):
        """Verify that highly innovative features bypass pure RICE for Kano excitement tracks."""
        self.state.tpm_profile.resource_constrained = False 
        self.state.tpm_profile.is_innovative = True # Triggers Kano
        
        # root -> innovative -> recommend_kano_model
        self.engine.run_layer_2()
        
        tpm = self.engine.state.architecture.tpm
        self.assertEqual(tpm["strategy"], "Kano Innovation Modeling")
        self.assertEqual(tpm["tier"], "recommend_kano_model")

    def test_rice_model(self):
        """Verify that stable metrics trigger RICE quantitative calculation."""
        self.state.tpm_profile.is_innovative = False
        self.state.tpm_profile.has_financial_impact = True # Triggers RICE
        self.state.tpm_profile.has_quantitative_metrics = True
        
        # root -> financial_impact -> recommend_rice_model
        self.engine.run_layer_2()
        
        tpm = self.engine.state.architecture.tpm
        self.assertEqual(tpm["strategy"], "RICE Quantitative Prioritization")
        self.assertEqual(tpm["tier"], "recommend_rice_model")

    def test_moscow_model(self):
        """Verify that ambiguous metrics fallback to MoSCoW qualitative definition."""
        self.state.tpm_profile.is_innovative = False
        self.state.tpm_profile.has_financial_impact = False # Triggers MoSCoW
        
        # root -> missing_metrics -> recommend_moscow_model
        self.engine.run_layer_2()
        
        tpm = self.engine.state.architecture.tpm
        self.assertEqual(tpm["strategy"], "MoSCoW Qualitative Classification")
        self.assertEqual(tpm["tier"], "recommend_moscow_model")

if __name__ == "__main__":
    unittest.main()
