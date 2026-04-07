"""DB Optimization Plugin (V55)."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class DBOptimizationPlugin(BaseDecisionTreePlugin):
    pillar_id = "db_optimization"
    name = "Database Optimization"
    category = "performance"

    @property
    def default_leaf(self) -> str:
        return "recommend_query_plan_analysis"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        is_supervised = metrics.get("is_psd2_scope") or metrics.get("is_bde_supervised")
        high_users = metrics.get("concurrent_users_val", 0) > 5000 or (getattr(getattr(state, "traffic_profile", None), "concurrent_users", 0) > 5000)
        requirements = getattr(state, "requirements", {})
        is_reporting = "reporting" in str(requirements).lower()
        
        return {
            "root": lambda m: (
                "deadlocks" if is_supervised
                else "connection_timeouts" if high_users
                else "high_latency" if m.get("latency_critical") or is_reporting
                else "high_latency"
            ),
            "deadlocks": lambda m: "yes",
            "query_type_check": lambda m: "reporting" if is_reporting else "single_lookup",
        }
