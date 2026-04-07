"""Team Structure Plugin (V63)."""
from typing import Any, Callable, Dict
from domain.ports.pillar_plugin import PillarPlugin, PillarResult
from domain.ports.knowledge_repository import KnowledgeRepository


class TeamStructurePlugin(PillarPlugin):
    """Non-standard tree: uses direct routing."""
    pillar_id = "team_structure"
    name = "Team Topology & Organizational Design"
    category = "organization"

    def __init__(self, knowledge_repo: KnowledgeRepository = None, **kwargs):
        self._repo = knowledge_repo

    def analyze(self, metrics: Dict[str, Any], state: Any) -> PillarResult:
        tree = self._repo.load("decision_tree") if self._repo else {"nodes": {"root": {"options": {}}}, "leaves": {}}

        tsp = getattr(state, "team_structure_profile", None)
        devs = getattr(tsp, "total_developers", 5) if tsp else 5
        reg = getattr(tsp, "regulatory_level", "low") if tsp else "low"

        if devs < 10: answer = "small_scale_startup"
        elif devs <= 40: answer = "mid_scale_transition"
        elif reg == "high": answer = "high_regulation_scale"
        else: answer = "high_scale_low_regulation"

        leaf_id = tree["nodes"]["root"]["options"].get(answer, answer)
        leaf = tree["leaves"].get(leaf_id, {"strategy": "Unknown", "reasoning": "", "pillars": []})

        return PillarResult(
            pillar_id=self.pillar_id,
            strategy=leaf["strategy"],
            tier=leaf_id,
            reasoning=leaf["reasoning"],
            details={"pillars": leaf.get("pillars", [])},
        )
