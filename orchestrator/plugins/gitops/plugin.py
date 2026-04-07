"""GitOps Plugin (V46)."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class GitOpsPlugin(BaseDecisionTreePlugin):
    pillar_id = "gitops"
    name = "GitOps Strategy"
    category = "operations"

    @property
    def default_leaf(self) -> str:
        return "recommend_standard_cicd"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        return {
            "root": lambda m: "yes",
            "deployment_frequency_check": lambda m: "yes"
            if m.get("scaling_problem") or m.get("is_psd2_scope") else "no",
            "multi_cluster_check": lambda m: "yes"
            if m.get("large_scale") or getattr(state, "raw_input", {}).get("multi_region_requested") else "no",
            "audit_requirement_check": lambda m: "yes"
            if m.get("is_bde_supervised") or m.get("is_gdpr_critical") else "no",
        }
