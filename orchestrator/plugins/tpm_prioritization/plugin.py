"""Technical Product Management Plugin (V57)."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class TPMPlugin(BaseDecisionTreePlugin):
    pillar_id = "tpm_prioritization"
    name = "Technical Product Management"
    category = "product"

    @property
    def default_leaf(self) -> str:
        return "recommend_moscow_model"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        tpm = getattr(state, "tpm_profile", None)
        blockers = getattr(tpm, "has_regulatory_blockers", False) if tpm else False
        resource = getattr(tpm, "resource_constrained", False) if tpm else False
        financials = getattr(tpm, "has_financial_impact", False) if tpm else False
        innovative = getattr(tpm, "is_innovative", False) if tpm else False
        quant = getattr(tpm, "has_quantitative_metrics", False) if tpm else False
        return {
            "root": lambda m: (
                "regulatory_blockers" if blockers
                else "resource_constrained" if resource
                else "innovative" if innovative
                else "financial_impact" if financials and quant
                else "missing_metrics"
            ),
        }
