import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestTeamStructureEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_flat_startup(self):
        """Verify routing for <10 devs."""
        self.state.team_structure_profile.total_developers = 8
        self.state.team_structure_profile.regulatory_level = "low"
        
        self.engine.run_layer_2()
        topology = self.engine.state.architecture.team_structure
        self.assertEqual(topology["tier"], "recommend_flat_generalist")

    def test_stream_aligned_transition(self):
        """Verify routing for 10-40 devs."""
        self.state.team_structure_profile.total_developers = 25
        self.state.team_structure_profile.regulatory_level = "low"
        
        self.engine.run_layer_2()
        topology = self.engine.state.architecture.team_structure
        self.assertEqual(topology["tier"], "recommend_stream_aligned_transition")

    def test_mature_platform(self):
        """Verify routing for >40 devs with low/medium regulation."""
        self.state.team_structure_profile.total_developers = 75
        self.state.team_structure_profile.regulatory_level = "medium"
        
        self.engine.run_layer_2()
        topology = self.engine.state.architecture.team_structure
        self.assertEqual(topology["tier"], "recommend_mature_platform_stream")

    def test_regulated_platform(self):
        """Verify routing for >40 devs with high regulation (Fintech context)."""
        self.state.team_structure_profile.total_developers = 60
        self.state.team_structure_profile.regulatory_level = "high"
        
        self.engine.run_layer_2()
        topology = self.engine.state.architecture.team_structure
        self.assertEqual(topology["tier"], "recommend_regulated_platform")

if __name__ == "__main__":
    unittest.main()
