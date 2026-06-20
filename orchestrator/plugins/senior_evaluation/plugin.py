"""Senior Evaluation Plugin."""
from typing import Any, Callable, Dict
from domain.ports.pillar_plugin import PillarPlugin, PillarResult
from domain.ports.knowledge_repository import KnowledgeRepository


class SeniorEvaluationPlugin(PillarPlugin):
    """Non-standard tree: uses weighted scoring instead of traversal."""
    pillar_id = "senior_evaluation"
    name = "Senior Talent Evaluation"
    category = "organization"

    def __init__(self, knowledge_repo: KnowledgeRepository = None, **kwargs):
        self._repo = knowledge_repo

    def analyze(self, metrics: Dict[str, Any], state: Any) -> PillarResult:
        tree = self._repo.load("decision_tree") if self._repo else {"nodes": {"root": {"options": {}}}, "leaves": {}}

        sep = getattr(state, "senior_eval_profile", None)
        sys_d = getattr(sep, "sys_design_score", 3.0) if sep else 3.0
        code = getattr(sep, "coding_score", 3.0) if sep else 3.0
        trade = getattr(sep, "tradeoff_score", 3.0) if sep else 3.0
        behav = getattr(sep, "behavioral_score", 3.0) if sep else 3.0
        comm = getattr(sep, "comm_score", 3.0) if sep else 3.0
        prod = getattr(sep, "product_score", 3.0) if sep else 3.0

        score = (sys_d * 0.35) + (code * 0.20) + (trade * 0.15) + (behav * 0.15) + (comm * 0.10) + (prod * 0.05)

        if score >= 4.5: answer = "score_staff_potential"
        elif score >= 3.8: answer = "score_solid_senior"
        elif score >= 3.2: answer = "score_mid_disguised"
        else: answer = "score_critical_reject"

        leaf_id = tree["nodes"]["root"]["options"].get(answer, answer)
        leaf = tree["leaves"].get(leaf_id, {"strategy": "Unknown", "reasoning": "", "pillars": []})

        return PillarResult(
            pillar_id=self.pillar_id,
            strategy=leaf["strategy"],
            tier=leaf_id,
            reasoning=f"Calculated Score: {score:.2f}. {leaf['reasoning']}",
            details={"pillars": leaf.get("pillars", []), "calculated_score": round(score, 2)},
        )
