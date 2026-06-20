"""Distributed Tracing Plugin."""
from typing import Any, Callable, Dict
from domain.ports.pillar_plugin import PillarResult
from plugins._base import BaseDecisionTreePlugin

class DistributedTracingPlugin(BaseDecisionTreePlugin):
    pillar_id = "distributed_tracing"
    name = "Distributed Tracing"
    category = "operations"

    @property
    def default_leaf(self) -> str:
        return "recommend_tracing_not_critical"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        high_load = metrics.get("large_scale") or metrics.get("scaling_problem") or metrics.get("concurrent_users_val", 0) > 5000
        return {
            "root": lambda m: "yes" if m.get("is_microservices") or m.get("is_psd2_scope") or m.get("is_fintech") or m.get("latency_critical") or high_load else "no",
            "issue_pattern_check": lambda m: "no" if high_load else ("yes" if m.get("latency_critical") else "no"),
            "tail_sampling_check": lambda m: "yes" if m.get("is_psd2_scope") or m.get("is_fintech") or m.get("is_bde_supervised") else "no",
            "resource_constraint_check": lambda m: "yes" if high_load else "no",
        }

    def build_result(self, leaf, ontology, metrics, state):
        return PillarResult(
            pillar_id=self.pillar_id,
            strategy=leaf.get("strategy", "Unknown"),
            tier=leaf.get("_leaf_id", "unknown"),
            reasoning=leaf.get("reasoning", ""),
            details={
                "sampling": leaf.get("sampling", ""),
                "recommended_pillars": leaf.get("pillars", []),
                "pillars": leaf.get("pillars", [])
            },
        )
