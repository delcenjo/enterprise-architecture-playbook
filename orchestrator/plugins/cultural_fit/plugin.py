"""Cultural Fit Plugin (V62)."""
from typing import Any, Callable, Dict
from domain.ports.pillar_plugin import PillarPlugin, PillarResult
from domain.ports.knowledge_repository import KnowledgeRepository


class CulturalFitPlugin(PillarPlugin):
    """Non-standard tree: uses weighted scoring instead of traversal."""
    pillar_id = "cultural_fit"
    name = "Cultural & Systemic Risk"
    category = "organization"

    def __init__(self, knowledge_repo: KnowledgeRepository = None, **kwargs):
        self._repo = knowledge_repo

    def analyze(self, metrics: Dict[str, Any], state: Any) -> PillarResult:
        tree = self._repo.load("decision_tree") if self._repo else {"nodes": {"root": {"options": {}}}, "leaves": {}}

        cfp = getattr(state, "cultural_fit_profile", None)
        own = getattr(cfp, "ownership_score", 3.0) if cfp else 3.0
        conf = getattr(cfp, "conflict_score", 3.0) if cfp else 3.0
        feed = getattr(cfp, "feedback_score", 3.0) if cfp else 3.0
        collab = getattr(cfp, "collaboration_score", 3.0) if cfp else 3.0
        transp = getattr(cfp, "transparency_score", 3.0) if cfp else 3.0
        learn = getattr(cfp, "learning_score", 3.0) if cfp else 3.0

        score = (own * 0.25) + (conf * 0.20) + (feed * 0.20) + (collab * 0.15) + (transp * 0.10) + (learn * 0.10)

        if score >= 4.5: answer = "score_multiplier"
        elif score >= 4.0: answer = "score_solid_fit"
        elif score >= 3.5: answer = "score_moderate_risk"
        else: answer = "score_high_friction"

        leaf_id = tree["nodes"]["root"]["options"].get(answer, answer)
        leaf = tree["leaves"].get(leaf_id, {"strategy": "Unknown", "reasoning": "", "pillars": []})

        return PillarResult(
            pillar_id=self.pillar_id,
            strategy=leaf["strategy"],
            tier=leaf_id,
            reasoning=f"Calculated Friction Score: {score:.2f}. {leaf['reasoning']}",
            details={"pillars": leaf.get("pillars", []), "calculated_score": round(score, 2)},
        )
