"""Frontend Performance Plugin."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class FrontendPerformancePlugin(BaseDecisionTreePlugin):
    pillar_id = "frontend_performance"
    name = "Frontend Performance"
    category = "performance"

    @property
    def default_leaf(self) -> str:
        return "recommend_lazy_load_cdn"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        users = getattr(getattr(state, "traffic_profile", None), "concurrent_users", 0)
        requirements = getattr(state, "requirements", {})
        services = requirements.get("services", [])
        return {
            "root": lambda m: (
                "high_fid" if "complex_analytics" in services or "high_interactivity" in services
                else "high_lcp" if users > 100000
                else "large_bundle"
            ),
            "ssr_vs_lazy_check": lambda m: "yes"
            if users > 100000 and not requirements.get("data_residency_required", False) else "no",
        }
