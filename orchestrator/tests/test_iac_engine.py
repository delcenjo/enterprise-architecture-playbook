import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestIaCEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_fintech_enterprise_terraform(self):
        """Verify that a critical fintech system gets Modular Terraform (Enterprise)."""
        self.state.raw_input = {
            "business_type": "FINTECH_HA",
            "is_bde_supervised": True
        }
        self.state.traffic_profile.concurrent_users = 100000 # large_scale
        
        self.engine.run_layer_2()
        
        iac = self.engine.state.architecture.iac
        self.assertEqual(iac["strategy"], "Modular Terraform (Enterprise Stack)")
        self.assertEqual(iac["tier"], "recommend_terraform_enterprise")
        self.assertIn("Terraform Modules", iac["pillars"])

    def test_saas_pulumi_cdk(self):
        """Verify that a standard SaaS with microservices gets Pulumi/CDK."""
        self.state.raw_input = {
            "business_type": "SAAS_STANDARD",
        }
        self.state.requirements = {"services": ["api", "worker"]} # microservices -> preference=yes
        
        self.engine.run_layer_2()
        
        iac = self.engine.state.architecture.iac
        # root=no (not large_scale), preference=yes (microservices)
        self.assertEqual(iac["strategy"], "Cloud Native IaC (Pulumi/CDK)")
        self.assertEqual(iac["tier"], "recommend_pulumi_cdk")

    def test_startup_standard_terraform(self):
        """Verify that a simple startup gets standard Terraform."""
        self.state.raw_input = {
            "business_type": "STARTUP_MVP"
        }
        # Not microservices, not multi-tenant
        
        self.engine.run_layer_2()
        
        iac = self.engine.state.architecture.iac
        self.assertEqual(iac["strategy"], "Standard Terraform")
        self.assertEqual(iac["tier"], "recommend_terraform_basic")

if __name__ == "__main__":
    unittest.main()
