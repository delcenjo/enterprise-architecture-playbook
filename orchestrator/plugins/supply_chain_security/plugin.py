"""Supply Chain Security Plugin."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class SupplyChainSecurityPlugin(BaseDecisionTreePlugin):
    pillar_id = "supply_chain_security"
    name = "Supply Chain Security"
    category = "operations"

    @property
    def default_leaf(self) -> str:
        return "recommend_basic_scanning"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        return {
            "root": lambda m: "yes"
            if m.get("is_psd2_scope") or m.get("is_bde_supervised") else "no",
            "slsa_requirement": lambda m: "yes"
            if m.get("large_scale") or m.get("latency_critical") else "no",
            "dependency_check": lambda m: "yes"
            if m.get("is_microservices") or m.get("multi_tenant") else "no",
            "cloud_native_check": lambda m: "yes"
            if getattr(state, "raw_input", {}).get("multi_region_requested") else "no",
        }
