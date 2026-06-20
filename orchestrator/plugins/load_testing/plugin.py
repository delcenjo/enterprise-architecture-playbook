"""Load Testing / Performance Engineering Plugin."""
from typing import Any, Callable, Dict
from plugins._base import BaseDecisionTreePlugin

class LoadTestingPlugin(BaseDecisionTreePlugin):
    pillar_id = "load_testing"
    name = "Performance Engineering"
    category = "performance"

    @property
    def default_leaf(self) -> str:
        return "recommend_standard_load"

    def build_question_map(self, metrics: Dict[str, Any], state: Any) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        is_ms = metrics.get("is_microservices") or "services" in str(getattr(state, "requirements", {})).lower()
        is_large = metrics.get("large_scale") or metrics.get("scaling_problem") or metrics.get("concurrent_users_val", 0) > 5000
        is_saas = "SAAS" in str(state.raw_input.get("business_type", "")).upper()
        is_supervised = metrics.get("is_psd2_scope") or metrics.get("is_bde_supervised")

        return {
            "root": lambda m: (
                "ensure_stability" if is_ms and is_large
                else "detect_limits" if is_supervised and is_large
                else "ci_cd_validation" if is_saas and not is_large
                else "detect_limits" if is_large
                else "ci_cd_validation"
            ),
            "is_it_sudden_spike": lambda m: "yes" if is_supervised else "no",
            "soak_test_check": lambda m: "yes" if is_ms or is_large else "no",
        }
