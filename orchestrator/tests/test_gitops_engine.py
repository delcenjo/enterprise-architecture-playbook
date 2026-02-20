import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestGitOpsEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_fintech_multi_cluster_gitops(self):
        """Verify that a multi-cluster fintech system gets ArgoCD GitOps."""
        self.state.raw_input = {
            "business_type": "FINTECH_HA",
            "multi_region_requested": True,
            "is_bde_supervised": True
        }
        self.state.traffic_profile.concurrent_users = 100000 # large_scale
        
        self.engine.run_layer_2()
        
        gitops = self.engine.state.architecture.gitops
        self.assertEqual(gitops["strategy"], "GitOps with ArgoCD (Full Sync)")
        self.assertEqual(gitops["tier"], "recommend_gitops_argocd")
        self.assertIn("Drift Detection", gitops["pillars"])

    def test_standard_saas_gitops(self):
        """Verify that a standard SaaS gets Flux GitOps due to audit needs."""
        self.state.raw_input = {
            "business_type": "SAAS_STANDARD",
        }
        # Not multi-region, but supervised or gdpr_critical
        self.state.compliance_profile.frameworks = ["GDPR"] 
        
        self.engine.run_layer_2()
        
        gitops = self.engine.state.architecture.gitops
        # root=Yes, freq=No (scaling_prob=No), audit=Yes (GDPR) -> Flux
        self.assertEqual(gitops["strategy"], "GitOps with Flux (Lightweight)")
        self.assertEqual(gitops["tier"], "recommend_gitops_flux")

    def test_startup_no_gitops(self):
        """Verify that a lean startup gets standard CI/CD."""
        self.state.raw_input = {
            "business_type": "STARTUP_MVP"
        }
        
        self.engine.run_layer_2()
        
        gitops = self.engine.state.architecture.gitops
        self.assertEqual(gitops["strategy"], "Standard CI/CD + IaC")
        self.assertEqual(gitops["tier"], "recommend_standard_cicd")

if __name__ == "__main__":
    unittest.main()
