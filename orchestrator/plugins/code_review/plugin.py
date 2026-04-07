"""Code Review Plugin (V54)."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class CodeReviewPlugin(BaseDecisionTreePlugin):
    pillar_id = "code_review"
    name = "Code Review Process"
    category = "engineering"

    @property
    def default_leaf(self) -> str:
        return "recommend_hybrid_scale"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        cr = getattr(state, "code_review_profile", None)
        has_ci = getattr(cr, "has_automated_ci", True) if cr else True
        gates = getattr(cr, "quality_gates_passing", True) if cr else True
        violations = getattr(cr, "critical_violations", 0) if cr else 0
        pr_size = getattr(cr, "pr_size_loc", 200) if cr else 200
        return {
            "root": lambda m: (
                "no_ci" if not has_ci
                else "gates_failing" if not gates
                else "critical_violations" if violations > 0
                else "massive_pr" if pr_size > 500
                else "passing_healthy"
            ),
        }
