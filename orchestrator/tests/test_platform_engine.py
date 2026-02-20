import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestPlatformEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_high_compliance(self):
        """Verify that high compliance needs mandate policy-enforced IDPs."""
        self.state.platform_profile.high_compliance_needs = True # Top priority
        self.state.platform_profile.team_size = 3
        
        # root -> high_compliance_regulated -> recommend_idp_policy_enforcement
        self.engine.run_layer_2()
        
        platform = self.engine.state.architecture.platform_engineering
        self.assertEqual(platform["strategy"], "Security-First IDP with Policy Enforcement")
        self.assertEqual(platform["tier"], "recommend_idp_policy_enforcement")

    def test_high_onboarding(self):
        """Verify that hypergrowth mandates automated onboarding workflows."""
        self.state.platform_profile.high_compliance_needs = False
        self.state.platform_profile.high_onboarding_frequency = True 
        
        # root -> high_onboarding_hypergrowth -> recommend_idp_automated_onboarding
        self.engine.run_layer_2()
        
        platform = self.engine.state.architecture.platform_engineering
        self.assertEqual(platform["strategy"], "IDP Optimized for Rapid Onboarding (Hypergrowth)")
        self.assertEqual(platform["tier"], "recommend_idp_automated_onboarding")

    def test_multi_stack_team(self):
        """Verify that highly diverse stacks mandate full IDP Golden Paths."""
        self.state.platform_profile.high_compliance_needs = False
        self.state.platform_profile.high_onboarding_frequency = False
        self.state.platform_profile.multiple_stacks = True
        self.state.platform_profile.team_size = 10
        
        # root -> large_team_multi_stack -> recommend_idp_multi_template
        self.engine.run_layer_2()
        
        platform = self.engine.state.architecture.platform_engineering
        self.assertEqual(platform["strategy"], "Deploy Full IDP + Multi-Stack Golden Paths")
        self.assertEqual(platform["tier"], "recommend_idp_multi_template")

    def test_small_team_standard(self):
        """Verify that small uniform teams fallback to standardized scripts/docs."""
        self.state.platform_profile.high_compliance_needs = False
        self.state.platform_profile.high_onboarding_frequency = False
        self.state.platform_profile.multiple_stacks = False
        self.state.platform_profile.team_size = 3
        
        # root -> small_team_standard_needs -> recommend_base_docs_scripts
        self.engine.run_layer_2()
        
        platform = self.engine.state.architecture.platform_engineering
        self.assertEqual(platform["strategy"], "Base Documentation & Automation Scripts")
        self.assertEqual(platform["tier"], "recommend_base_docs_scripts")

if __name__ == "__main__":
    unittest.main()
