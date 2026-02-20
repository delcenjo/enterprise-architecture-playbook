import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestSupplyChainEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_fintech_full_supply_chain(self):
        """Verify that a critical fintech system gets SLSA L3 protection."""
        self.state.raw_input = {
            "business_type": "FINTECH_HA",
            "is_bde_supervised": True
        }
        self.state.traffic_profile.concurrent_users = 100000 # large_scale -> slsa_req=yes
        
        self.engine.run_layer_2()
        
        supply = self.engine.state.architecture.supply_chain
        self.assertEqual(supply["strategy"], "Full Supply Chain Protection (SLSA L3)")
        self.assertEqual(supply["tier"], "recommend_full_supply_chain")
        self.assertIn("SBOM (CycloneDX)", supply["pillars"])

    def test_standard_saas_sbom(self):
        """Verify that a standard SaaS with microservices gets SBOM."""
        self.state.raw_input = {
            "business_type": "SAAS_STANDARD",
        }
        self.state.requirements = {"services": ["auth", "payments"]} # microservices -> dep_check=yes
        
        self.engine.run_layer_2()
        
        supply = self.engine.state.architecture.supply_chain
        self.assertEqual(supply["strategy"], "SBOM & Dependency Scanning")
        self.assertEqual(supply["tier"], "recommend_sbom_scanning")

    def test_lean_startup_basic_scans(self):
        """Verify that a lean startup gets basic scanning."""
        self.state.raw_input = {
            "business_type": "STARTUP_MVP"
        }
        
        self.engine.run_layer_2()
        
        supply = self.engine.state.architecture.supply_chain
        self.assertEqual(supply["strategy"], "Basic Dependency Scanning")
        self.assertEqual(supply["tier"], "recommend_basic_scanning")

if __name__ == "__main__":
    unittest.main()
