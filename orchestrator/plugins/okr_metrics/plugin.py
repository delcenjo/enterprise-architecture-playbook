"""Technical OKRs Plugin (V58)."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class OKRPlugin(BaseDecisionTreePlugin):
    pillar_id = "okr_metrics"
    name = "Technical OKRs & DORA"
    category = "product"

    @property
    def default_leaf(self) -> str:
        return "recommend_operational_maintenance"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        okr = getattr(state, "okr_profile", None)
        mttr = getattr(okr, "mttr_high", False) if okr else False
        fail = getattr(okr, "change_failure_rate_high", False) if okr else False
        freq = getattr(okr, "deployment_frequency_low", False) if okr else False
        lead = getattr(okr, "lead_time_high", False) if okr else False
        quality = getattr(okr, "quality_degradation", False) if okr else False
        strategic = getattr(okr, "strategic_business_goal_active", False) if okr else False
        return {
            "root": lambda m: (
                "high_failure_rate_or_mttr" if mttr or fail
                else "low_deployment_frequency" if freq or lead
                else "strategic_business_goal" if strategic
                else "quality_degradation" if quality
                else "stable_metrics"
            ),
        }
