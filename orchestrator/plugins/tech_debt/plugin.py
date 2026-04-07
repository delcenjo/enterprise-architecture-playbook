"""Technical Debt Plugin (V53)."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class TechDebtPlugin(BaseDecisionTreePlugin):
    pillar_id = "tech_debt"
    name = "Technical Debt Analysis"
    category = "engineering"

    @property
    def default_leaf(self) -> str:
        return "recommend_incremental_refactor"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        td = getattr(state, "tech_debt_profile", None)
        tp = getattr(state, "traffic_profile", None)
        sqale = getattr(td, "sqale_index", 10.0) if td else 10.0
        climate = getattr(td, "code_climate", 4.0) if td else 4.0
        coverage = getattr(td, "test_coverage", 80.0) if td else 80.0
        complexity = getattr(td, "cyclomatic_complexity", 5) if td else 5
        rps = getattr(tp, "requests_per_second", 0) if tp else 0
        return {
            "root": lambda m: (
                "critical_debt" if sqale < 4.0 or climate < 2.0
                else "low_coverage" if coverage < 60.0
                else "high_complexity" if complexity > 15
                else "manageable_debt"
            ),
            "business_impact_check": lambda m: "yes"
            if rps > 5000 or m.get("latency_critical") or m.get("strict_governance") else "no",
        }
