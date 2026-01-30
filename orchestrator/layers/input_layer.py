import json
import os
import logging
import pandas as pd
from functools import lru_cache
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from global_state import GlobalState, TrafficProfile, DataProfile, ComplianceProfile, DataSensitivity

# Setup structured logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Layer1_Normalizer")

class ProjectContext(BaseModel):
    company_type: str = "Enterprise"
    industry: str = "General"
    countries_of_operation: List[str] = Field(default_factory=list)
    product_phase: str = "Scaling"

    @field_validator('industry')
    @classmethod
    def validate_industry(cls, v: str) -> str:
        return v

class CurrentArchitecture(BaseModel):
    architecture_type: str = "Monolith"
    cloud_provider: str = "AWS"
    tenancy_model: str = "Single-tenant"
    primary_database: str = "PostgreSQL"
    messaging_system: str = "None"
    observability_level: str = "Basic"
    cicd_maturity: str = "Manual"

class ScaleAndLoad(BaseModel):
    monthly_active_users: int = 10000
    peak_concurrent_users: int = 500
    estimated_rps: float = 50.0
    current_p95_latency_ms: float = 500.0
    expected_mom_growth_pct: float = 5.0
    active_regions: int = 1
    target_sla: str = "99.9%"

class DataAndSensitivity(BaseModel):
    processes_pii: bool = False
    special_categories: bool = False
    processes_payments: bool = False
    regulated_entity: bool = False
    data_retention_years: float = 5.0
    cross_border_transfers: bool = False

class TeamAndOrganization(BaseModel):
    total_developers: int = 10
    total_sre_devops: int = 1
    has_platform_team: bool = False
    average_seniority: str = "Mid"
    deployment_frequency: str = "Weekly"
    approximate_mttr: str = "Hours"

class Financials(BaseModel):
    annual_revenue: float = 1000000.0
    monthly_burn_rate: float = 50000.0
    cloud_cost_pct_of_revenue: float = 10.0
    cac: float = 100.0
    churn_rate_pct: float = 5.0
    gross_margin_pct: float = 70.0

class UserObjectives(BaseModel):
    strategic_goals: List[str] = Field(default_factory=list)
    primary_problem_description: str = ""

class EnterpriseDecisionInput(BaseModel):
    project_context: ProjectContext = Field(default_factory=ProjectContext)
    current_architecture: CurrentArchitecture = Field(default_factory=CurrentArchitecture)
    scale_and_load: ScaleAndLoad = Field(default_factory=ScaleAndLoad)
    data_and_sensitivity: DataAndSensitivity = Field(default_factory=DataAndSensitivity)
    team_and_organization: TeamAndOrganization = Field(default_factory=TeamAndOrganization)
    financials: Financials = Field(default_factory=Financials)
    user_objectives: UserObjectives = Field(default_factory=UserObjectives)

@lru_cache(maxsize=1)
def load_normalization_assets():
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    
    # Load Factors
    factors_path = os.path.join(assets_dir, "normalization_factors.json")
    with open(factors_path, 'r') as f:
        factors = json.load(f)
        
    # Load Benchmarks
    benchmarks_path = os.path.join(assets_dir, "benchmarks.csv")
    benchmarks = pd.read_csv(benchmarks_path)
    
    return factors, benchmarks

class PipelineManager:
    def __init__(self):
        self.state = GlobalState()

    def run_layer_0_and_1(self, input_data: Dict[str, Any]):
        """
        Layer 0: Advanced Validation
        Layer 1: Data-Driven Normalization
        """
        logger.info("Starting Layer 0: Contextual Validation...")
        try:
            validated_input = EnterpriseDecisionInput(**input_data)
            self.state.raw_input = validated_input.dict()
        except ValidationError as e:
            logger.error(f"Validation Failure: {e}")
            raise ValueError(f"Strict Validation Failed: {e.json()}")

        logger.info("Starting Layer 1: Data-Driven Normalization...")
        
        # 1. Traffic Normalization (Configurable)
        growth_rate = validated_input.scale_and_load.expected_mom_growth_pct / 100.0
        self.state.traffic_profile = TrafficProfile(
            concurrent_users=validated_input.scale_and_load.peak_concurrent_users,
            growth_rate=growth_rate,
            requests_per_second=validated_input.scale_and_load.estimated_rps
        )

        # 2. Data Normalization (Benchmark-based)
        sensitivity_val = DataSensitivity.MEDIUM
        if validated_input.data_and_sensitivity.regulated_entity or validated_input.data_and_sensitivity.processes_payments:
            sensitivity_val = DataSensitivity.CRITICAL
        elif validated_input.data_and_sensitivity.processes_pii:
            sensitivity_val = DataSensitivity.HIGH
        
        # approximate gb per month based on MAU
        volume_gb = validated_input.scale_and_load.monthly_active_users * 0.05
        
        self.state.data_profile = DataProfile(
            sensitivity=sensitivity_val,
            volume_gb=float(volume_gb),
            retention_days=int(validated_input.data_and_sensitivity.data_retention_years * 365)
        )

        # 3. Compliance Normalization
        frameworks = []
        if validated_input.data_and_sensitivity.regulated_entity:
            frameworks.append("DORA")
        if validated_input.data_and_sensitivity.processes_pii:
            frameworks.append("GDPR")
        if validated_input.data_and_sensitivity.processes_payments:
            frameworks.append("PSD2")
            frameworks.append("PCI-DSS")
            
        region = "EU" if "España" in validated_input.project_context.countries_of_operation else "US"
        
        self.state.compliance_profile = ComplianceProfile(
            frameworks=frameworks,
            required_region=region,
            currency="EUR" if region == "EU" else "USD",
            availability_target=validated_input.scale_and_load.target_sla
        )
        
        # 4. Team Structure Normalization
        self.state.team_structure_profile.total_developers = validated_input.team_and_organization.total_developers
        self.state.team_structure_profile.platform_maturity = "mature" if validated_input.team_and_organization.has_platform_team else "none"
        self.state.team_structure_profile.regulatory_level = "high" if validated_input.data_and_sensitivity.regulated_entity else "low"

        logger.info(f"Layer 1 Complete. Traffic: {self.state.traffic_profile.concurrent_users} users, Data: {self.state.data_profile.volume_gb:.2f} GB")
        return "Requirements normalized with advanced intelligence"

if __name__ == "__main__":
    manager = PipelineManager()
    
    test_input = {
        "project_context": {
            "company_type": "Startup",
            "industry": "Fintech",
            "countries_of_operation": ["España"],
            "product_phase": "Scaling"
        },
        "current_architecture": {
            "architecture_type": "Monolith",
            "cloud_provider": "AWS",
            "tenancy_model": "Single-tenant",
            "primary_database": "PostgreSQL",
            "messaging_system": "None",
            "observability_level": "Basic",
            "cicd_maturity": "Basic"
        },
        "scale_and_load": {
            "monthly_active_users": 50000,
            "peak_concurrent_users": 1500,
            "estimated_rps": 120.0,
            "current_p95_latency_ms": 350.0,
            "expected_mom_growth_pct": 10.0,
            "active_regions": 1,
            "target_sla": "99.99%"
        },
        "data_and_sensitivity": {
            "processes_pii": True,
            "special_categories": False,
            "processes_payments": True,
            "regulated_entity": True,
            "data_retention_years": 10.0,
            "cross_border_transfers": False
        },
        "team_and_organization": {
            "total_developers": 25,
            "total_sre_devops": 2,
            "has_platform_team": False,
            "average_seniority": "Mid",
            "deployment_frequency": "Weekly",
            "approximate_mttr": "Hours"
        },
        "financials": {
            "annual_revenue": 5000000.0,
            "monthly_burn_rate": 200000.0,
            "cloud_cost_pct_of_revenue": 8.0,
            "cac": 150.0,
            "churn_rate_pct": 3.0,
            "gross_margin_pct": 80.0
        },
        "user_objectives": {
            "strategic_goals": ["Escalar sin romper", "Mejorar DORA metrics", "Prepararse para auditoría"],
            "primary_problem_description": "We need to break the monolith to satisfy BdE scaling constraints."
        }
    }
    print("\n--- TEST: Enterprise Decision Input ---")
    manager.run_layer_0_and_1(test_input)
    print(manager.state.model_dump_json(indent=2))
