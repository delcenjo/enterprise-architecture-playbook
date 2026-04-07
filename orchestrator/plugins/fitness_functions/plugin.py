"""Architectural Fitness Functions Plugin (V55)."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class FitnessFunctionsPlugin(BaseDecisionTreePlugin):
    pillar_id = "fitness_functions"
    name = "Architectural Fitness Functions"
    category = "engineering"

    @property
    def default_leaf(self) -> str:
        return "recommend_partial_checks"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        af = getattr(state, "arch_fitness_profile", None)
        crit = getattr(af, "critical_violations", 0) if af else 0
        services = getattr(af, "services_modified", 1) if af else 1
        drift = getattr(af, "drift_rate", 0.0) if af else 0.0
        comp = getattr(af, "compliance_score", 100.0) if af else 100.0
        mod_v = getattr(af, "modularity_violated", False) if af else False
        return {
            "root": lambda m: (
                "critical_violations" if crit > 0
                else "broad_blast_radius" if services > 5
                else "high_drift" if drift > 10.0
                else "modularity_violation" if mod_v
                else "low_compliance" if comp < 80.0
                else "healthy_state"
            ),
        }
