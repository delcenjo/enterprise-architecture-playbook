"""Profiling Engineering Plugin."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class ProfilingPlugin(BaseDecisionTreePlugin):
    pillar_id = "profiling"
    name = "Profiling Engineering"
    category = "performance"

    @property
    def default_leaf(self) -> str:
        return "recommend_lightweight_cpu"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        users = getattr(getattr(state, "traffic_profile", None), "concurrent_users", 0)
        return {
            "root": lambda m: (
                "high_latency" if m.get("is_microservices") and m.get("latency_critical")
                else "increasing_memory" if users > 10000
                else "general_slowness"
            ),
            "cpu_or_io_check": lambda m: "io_bound"
            if m.get("large_scale") and m.get("schema_evolution_risk") else "cpu_bound",
            "production_safety_check": lambda m: "yes"
            if m.get("is_bde_supervised") or m.get("is_psd2_scope") else "no",
        }
