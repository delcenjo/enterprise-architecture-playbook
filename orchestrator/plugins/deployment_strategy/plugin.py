"""Deployment Strategy Plugin (V45)."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class DeploymentStrategyPlugin(BaseDecisionTreePlugin):
    pillar_id = "deployment_strategy"
    name = "Deployment Strategy"
    category = "operations"

    @property
    def default_leaf(self) -> str:
        return "recommend_standard_rolling"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        return {
            "root": lambda m: "yes"
            if m.get("is_psd2_scope") or m.get("latency_critical") else "no",
            "scale_check": lambda m: "yes"
            if m.get("is_bde_supervised") or m.get("large_scale") else "no",
            "canary_check": lambda m: "yes"
            if m.get("large_scale") or m.get("is_microservices") else "no",
            "feature_flag_check": lambda m: "yes"
            if m.get("is_gdpr_critical") or m.get("multi_tenant") else "no",
        }
