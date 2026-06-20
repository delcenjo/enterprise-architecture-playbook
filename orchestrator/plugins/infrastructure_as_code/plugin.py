"""Infrastructure as Code Plugin."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class InfrastructureAsCodePlugin(BaseDecisionTreePlugin):
    pillar_id = "infrastructure_as_code"
    name = "Infrastructure as Code"
    category = "operations"

    @property
    def default_leaf(self) -> str:
        return "recommend_terraform_basic"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        return {
            "root": lambda m: "yes"
            if m.get("large_scale") or getattr(state, "raw_input", {}).get("multi_region_requested") else "no",
            "terraform_mandate": lambda m: "yes"
            if m.get("is_psd2_scope") or m.get("is_bde_supervised") else "no",
            "language_preference_check": lambda m: "yes"
            if m.get("is_microservices") or m.get("multi_tenant") else "no",
        }
