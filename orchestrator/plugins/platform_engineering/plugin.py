"""Platform Engineering Plugin."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class PlatformEngineeringPlugin(BaseDecisionTreePlugin):
    pillar_id = "platform_engineering"
    name = "Platform Engineering (Developer Experience)"
    category = "organization"

    @property
    def default_leaf(self) -> str:
        return "recommend_base_docs_scripts"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        pp = getattr(state, "platform_profile", None)
        team_size = getattr(pp, "team_size", 2) if pp else 2
        multistack = getattr(pp, "multiple_stacks", False) if pp else False
        compliance = getattr(pp, "high_compliance_needs", False) if pp else False
        onboarding = getattr(pp, "high_onboarding_frequency", False) if pp else False
        return {
            "root": lambda m: (
                "high_compliance_regulated" if compliance
                else "high_onboarding_hypergrowth" if onboarding
                else "large_team_multi_stack" if team_size > 5 or multistack
                else "small_team_standard_needs"
            ),
        }
