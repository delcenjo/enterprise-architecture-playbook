"""Chaos Engineering Plugin."""
from typing import Any, Callable, Dict
from domain.ports.pillar_plugin import PillarResult
from plugins._base import BaseDecisionTreePlugin

class ChaosEngineeringPlugin(BaseDecisionTreePlugin):
    pillar_id = "chaos_engineering"
    name = "Chaos Engineering"
    category = "operations"

    @property
    def default_leaf(self) -> str:
        return "recommend_traditional_testing"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        return {
            "root": lambda m: "yes"
            if m.get("is_microservices") or m.get("is_psd2_scope") or "SAAS" in state.raw_input.get("business_type", "").upper() else "no",
            "team_maturity_check": lambda m: "yes"
            if m.get("is_bde_supervised") or m.get("large_scale") else "no",
            "experiment_goal_check": lambda m: "validate_resilience",
            "risk_tolerance_check": lambda m: "yes"
            if m.get("large_scale") and m.get("is_bde_supervised") else "no",
        }

    def build_result(self, leaf, ontology, metrics, state):
        return PillarResult(
            pillar_id=self.pillar_id,
            strategy=leaf.get("strategy", "Unknown"),
            tier=leaf.get("_leaf_id", "unknown"),
            reasoning=leaf.get("reasoning", ""),
            details={
                "scope": leaf.get("scope", ""),
                "recommended_pillars": leaf.get("pillars", []),
                "pillars": leaf.get("pillars", []) # include both to be safe
            },
        )
