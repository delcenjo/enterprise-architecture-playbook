"""Tradeoff Analysis Plugin."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class TradeoffAnalysisPlugin(BaseDecisionTreePlugin):
    pillar_id = "tradeoff_analysis"
    name = "Build vs Buy Tradeoff Analysis"
    category = "product"

    @property
    def default_leaf(self) -> str:
        return "recommend_standard_evaluation"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        tp = getattr(state, "tradeoff_profile", None)
        core = getattr(tp, "is_core_business", False) if tp else False
        ttm = getattr(tp, "time_to_market_critical", False) if tp else False
        saas = getattr(tp, "mature_saas_available", False) if tp else False
        budget = getattr(tp, "budget_constrained", False) if tp else False
        ltm = getattr(tp, "long_term_maintenance_critical", False) if tp else False
        return {
            "root": lambda m: (
                "core_business_time_critical" if core and ttm
                else "non_core_saas_available" if saas and not core
                else "core_long_term_critical" if core and ltm
                else "non_core_budget_constrained" if not core and budget
                else "balanced_standard"
            ),
        }
