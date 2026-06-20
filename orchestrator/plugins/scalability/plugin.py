"""Scalability Analysis Plugin."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class ScalabilityPlugin(BaseDecisionTreePlugin):
    pillar_id = "scalability"
    name = "Scalability Predictive Analysis"
    category = "engineering"

    @property
    def default_leaf(self) -> str:
        return "recommend_continuous_monitoring"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        sp = getattr(state, "scalability_profile", None)
        pred = getattr(sp, "predicted_traffic_percent", 0.0) if sp else 0.0
        queue = getattr(sp, "queue_length_critical", False) if sp else False
        cpu_io = getattr(sp, "cpu_io_saturation_percent", 0.0) if sp else 0.0
        latency_v = getattr(sp, "latency_p99_violates_sla", False) if sp else False
        return {
            "root": lambda m: (
                "high_predictive_traffic" if pred > 90.0
                else "queue_saturation" if queue
                else "cpu_io_saturation" if cpu_io > 80.0
                else "latency_breach" if latency_v
                else "healthy_metrics"
            ),
        }
