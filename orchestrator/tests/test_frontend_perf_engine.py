import unittest
from global_state import GlobalState
from layers.core_engine import CoreEngine

class TestFrontendPerfEngine(unittest.TestCase):
    def setUp(self):
        self.state = GlobalState()
        self.engine = CoreEngine(self.state)

    def test_high_interactivity_spa(self):
        """Verify that a highly interactive app gets code splitting (FID fix)."""
        self.state.raw_input = {
            "application_type": "web",
            "business_type": "SAAS_STANDARD",
        }
        self.state.requirements = {"services": ["high_interactivity", "dashboard"]}
        self.engine.run_layer_2()
        
        front = self.engine.state.architecture.frontend_perf
        self.assertEqual(front["strategy"], "Code Splitting & Main Thread Offloading")
        self.assertEqual(front["tier"], "recommend_code_splitting")

    def test_large_scale_public_ssr(self):
        """Verify that a massive scale public site gets SSR (SEO/LCP fix)."""
        self.state.raw_input = {
            "application_type": "web",
            "business_type": "MEDIA_PUBLISHING"
        }
        self.state.traffic_profile.requests_per_second = 15000
        self.state.traffic_profile.concurrent_users = 200000
        self.state.requirements = {"services": ["public_content"]}
        self.engine.run_layer_2()
        
        front = self.engine.state.architecture.frontend_perf
        self.assertEqual(front["strategy"], "Server-Side Rendering (SSR) & Edge Compute")
        self.assertEqual(front["tier"], "recommend_ssr_edge")

    def test_standard_lazy_loading(self):
        """Verify default fallback to lazy loading for normal LCP issues."""
        self.state.raw_input = {
            "application_type": "web",
            "business_type": "STARTUP_MVP"
        }
        self.state.traffic_profile.requests_per_second = 500
        self.state.traffic_profile.concurrent_users = 150000
        self.state.requirements = {"data_residency_required": True}  # SSR excluded when data residency is required
        self.engine.run_layer_2()
        
        front = self.engine.state.architecture.frontend_perf
        self.assertEqual(front["strategy"], "Lazy Loading & CDN Edge Caching")
        self.assertEqual(front["tier"], "recommend_lazy_load_cdn")

if __name__ == "__main__":
    unittest.main()
