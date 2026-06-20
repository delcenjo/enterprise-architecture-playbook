import asyncio
import os
import json
from typing import Dict, Any
from layers.input_layer import PipelineManager
from layers.core_engine import CoreEngine
from layers.calculation_engine import CalculationEngine
from layers.visual_engine import VisualEngine
from layers.validation_layer import ValidationLayer
from layers.narrative_engine import NarrativeEngine

class IntelligentDossierForge:
    """
    Final Orchestrator for the 6-Layer Deterministic Architecture.
    """
    def __init__(self):
        self.manager = PipelineManager()

    async def execute_pipeline(self, input_data: Dict[str, Any]):
        print("Starting Revolutionized 6-Layer Deterministic Pipeline...")
        
        # Layer 0 & 1: Normalization
        self.manager.run_layer_0_and_1(input_data)
        print("Layer 1: Contextual Validation & Normalization Complete.")

        # Layer 2: Core Engine
        from layers.core_engine import CoreEngine
        CoreEngine(self.manager.state).run_layer_2()
        print("Layer 2: Adaptive Architecture & Component Injection Complete.")

        # Layer 3: Calculation Engine
        from layers.calculation_engine import CalculationEngine
        CalculationEngine(self.manager.state).run_layer_3()
        print("Layer 3: Precise Pricing & Scenario Analysis Complete.")

        # Layer 4: Visual Engine
        from layers.visual_engine import VisualEngine
        VisualEngine(self.manager.state).run_layer_4()
        print("Layer 4: High-Res Clustered Visuals Generated.")

        # Layer 5: Validation & Audit
        from layers.validation_layer import ValidationLayer
        ValidationLayer(self.manager.state).run_layer_5()
        print(f"Layer 5: Technical Audit & Integrity Seal Generated. Compliance: {self.manager.state.compliance_score}%")

        # Layer 6: Narrative Engine
        from layers.narrative_engine import NarrativeEngine
        narrative_engine = NarrativeEngine(self.manager.state)
        results = await narrative_engine.generate_premium_dossier()
        print(f"Layer 6: Premium Institutional Dossier forged (HTML & PDF).")

        return results, self.manager.state

if __name__ == "__main__":
    high_stakes_input = {
        "project_context": {
            "company_type": "Enterprise",
            "industry": "Fintech",
            "countries_of_operation": ["España", "France", "Germany"],
            "product_phase": "Scaling"
        },
        "current_architecture": {
            "architecture_type": "Monolith",
            "cloud_provider": "AWS",
            "tenancy_model": "Single-tenant",
            "primary_database": "PostgreSQL",
            "messaging_system": "None",
            "observability_level": "Intermediate",
            "cicd_maturity": "Semi-automated"
        },
        "scale_and_load": {
            "monthly_active_users": 500000,
            "peak_concurrent_users": 15000,
            "estimated_rps": 2000.0,
            "current_p95_latency_ms": 150.0,
            "expected_mom_growth_pct": 20.0,
            "active_regions": 3,
            "target_sla": "99.99%"
        },
        "data_and_sensitivity": {
            "processes_pii": True,
            "special_categories": True,
            "processes_payments": True,
            "regulated_entity": True,
            "data_retention_years": 10.0,
            "cross_border_transfers": True
        },
        "team_and_organization": {
            "total_developers": 120,
            "total_sre_devops": 15,
            "has_platform_team": True,
            "average_seniority": "Senior",
            "deployment_frequency": "Daily",
            "approximate_mttr": "Minutes"
        },
        "financials": {
            "annual_revenue": 100000000.0,
            "monthly_burn_rate": 5000000.0,
            "cloud_cost_pct_of_revenue": 15.0,
            "cac": 300.0,
            "churn_rate_pct": 2.0,
            "gross_margin_pct": 65.0
        },
        "user_objectives": {
            "strategic_goals": ["Mejorar DORA metrics", "Escalar sin romper", "Internacionalizar"],
            "primary_problem_description": "We need to decompose the monolith to support European expansion and comply with DORA."
        }
    }
    forge = IntelligentDossierForge()
    try:
        results, state = asyncio.run(forge.execute_pipeline(high_stakes_input))
        print(f"\nMISSION ACCOMPLISHED: Final Dossier generated at:")
        print(f"HTML: {results['html']}")
        print(f"PDF: {results['pdf']}")
        print(f"Integrity Seal: {state.costs.get('state_integrity_seal')}")
    except Exception as e:
        print(f"Pipeline Failure: {e}")
        import traceback
        traceback.print_exc()
