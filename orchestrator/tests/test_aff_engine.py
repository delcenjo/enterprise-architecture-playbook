import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestAFFEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_critical_violations(self):
        """Verify that catastrophic architectural flaws trigger senior escalation and merge block."""
        self.state.arch_fitness_profile.critical_violations = 1
        self.state.arch_fitness_profile.services_modified = 10
        self.engine.run_layer_2()
        
        aff = self.engine.state.architecture.aff
        self.assertEqual(aff["strategy"], "Block Merge & Architect Escalation")
        self.assertEqual(aff["tier"], "recommend_block_escalate")

    def test_broad_blast_radius(self):
        """Verify that a massive multi-service PR triggers full AFF validation."""
        self.state.arch_fitness_profile.critical_violations = 0
        self.state.arch_fitness_profile.services_modified = 8
        self.engine.run_layer_2()
        
        aff = self.engine.state.architecture.aff
        self.assertEqual(aff["strategy"], "Execute Full Suite of Fitness Functions")
        self.assertEqual(aff["tier"], "recommend_full_aff")

    def test_high_drift(self):
        """Verify that drift over 10% blocks new features for a refactor sprint."""
        self.state.arch_fitness_profile.services_modified = 2
        self.state.arch_fitness_profile.drift_rate = 12.5
        self.engine.run_layer_2()
        
        aff = self.engine.state.architecture.aff
        self.assertEqual(aff["strategy"], "Architectural Refactor Mandate")
        self.assertEqual(aff["tier"], "recommend_refactor_plan")

    def test_modularity_violation(self):
        """Verify that minor coupling trips an async team alert."""
        self.state.arch_fitness_profile.drift_rate = 5.0
        self.state.arch_fitness_profile.modularity_violated = True
        self.engine.run_layer_2()
        
        aff = self.engine.state.architecture.aff
        self.assertEqual(aff["strategy"], "Asynchronous Modularity Alert")
        self.assertEqual(aff["tier"], "recommend_alert_team")

    def test_low_compliance_score(self):
        """Verify that sub-80 compliance generates risk reports."""
        self.state.arch_fitness_profile.modularity_violated = False
        self.state.arch_fitness_profile.compliance_score = 72.0
        self.state.arch_fitness_profile.drift_rate = 8.0
        self.engine.run_layer_2()
        
        aff = self.engine.state.architecture.aff
        self.assertEqual(aff["strategy"], "Generate Automated Risk Report")
        self.assertEqual(aff["tier"], "recommend_risk_report")

    def test_healthy_state(self):
        """Verify that optimal architectures pass with standard checks."""
        self.state.arch_fitness_profile.services_modified = 1
        self.state.arch_fitness_profile.modularity_violated = False
        self.state.arch_fitness_profile.compliance_score = 98.0
        self.state.arch_fitness_profile.drift_rate = 1.0
        self.engine.run_layer_2()
        
        aff = self.engine.state.architecture.aff
        self.assertEqual(aff["strategy"], "Execute Partial / Quick Constraints")
        self.assertEqual(aff["tier"], "recommend_partial_checks")

if __name__ == "__main__":
    unittest.main()
