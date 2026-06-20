"""Observability Stack Plugin."""
from typing import Any, Callable, Dict
from domain.ports.pillar_plugin import PillarResult
from plugins._base import BaseDecisionTreePlugin


class ObservabilityPlugin(BaseDecisionTreePlugin):
    pillar_id = "observability"
    name = "Observability Stack"
    category = "operations"

    @property
    def default_leaf(self) -> str:
        return "recommend_metrics_logs_basic"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        return {
            "root": lambda m: "start",
            "high_criticality_check": lambda m: "no" if m.get("is_microservices") else ("yes" if m.get("scaling_problem") or m.get("is_psd2_scope") else "no"),
            "distributed_check": lambda m: "yes" if m.get("is_microservices") else "no",
            "regulatory_check": lambda m: "yes"
            if m.get("is_gdpr_critical") or m.get("is_aml_scope") else "no",
        }

    def build_result(self, leaf, ontology, metrics, state):
        stack = {
            "recommendation_id": leaf.get("_leaf_id"),
            "pillars": leaf.get("pillars", []),
            "features": leaf.get("features", []),
            "reasoning": leaf.get("reasoning", ""),
            "tools": [],
            "total_estimated_cost": 0,
        }
        for p in leaf.get("pillars", []):
            p_data = ontology.get(p, {})
            tools = p_data.get("herramientas", [])
            if isinstance(tools, list):
                stack["tools"].extend(tools)
            stack["total_estimated_cost"] += p_data.get("coste_estimado", 0)

        return PillarResult(
            pillar_id=self.pillar_id,
            strategy=leaf.get("strategy", stack.get("recommendation_id", "Unknown")),
            tier=leaf.get("_leaf_id", "unknown"),
            reasoning=leaf.get("reasoning", ""),
            details=stack,
        )
