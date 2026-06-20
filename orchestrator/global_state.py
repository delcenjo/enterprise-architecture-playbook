from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class DataSensitivity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @property
    def impact_score(self) -> int:
        scores = {"low": 1, "medium": 2, "high": 3, "critical": 5}
        return scores.get(self.value, 2)

class TrafficProfile(BaseModel):
    concurrent_users: int = 0
    peak_factor: float = 3.0
    growth_rate: float = 0.0
    requests_per_second: float = 0.0
    rps_per_user: float = 0.01
    egress_gb_month: float = 0.0 

class DataProfile(BaseModel):
    volume_gb: float = 0.0
    sensitivity: DataSensitivity = DataSensitivity.MEDIUM
    daily_growth_mb: float = 0.0
    iops_required: int = 3000 # New: IOPS benchmarks
    retention_days: int = 365 # New: For tiering logic

class TechDebtProfile(BaseModel):
    sqale_index: float = 10.0 # 0-10, lower is worse
    code_climate: float = 4.0 # 0-4, lower is worse
    test_coverage: float = 80.0 # Percentage
    cyclomatic_complexity: int = 5 # Average per module

class CodeReviewProfile(BaseModel):
    has_automated_ci: bool = True
    quality_gates_passing: bool = True
    critical_violations: int = 0
    pr_size_loc: int = 200 # Average lines of code per PR

class ArchFitnessProfile(BaseModel):
    services_modified: int = 1
    critical_violations: int = 0
    drift_rate: float = 0.0 # Percentage 0-100
    compliance_score: float = 100.0 # Percentage 0-100
    modularity_violated: bool = False

class ScalabilityProfile(BaseModel):
    traffic_saturation_percent: float = 50.0 # Current vs Max 0-100
    queue_length_critical: bool = False
    cpu_io_saturation_percent: float = 50.0 # Hardware limits 0-100
    latency_p99_violates_sla: bool = False
    predicted_traffic_percent: float = 60.0 # Forecast peak traffic 0-100

class TPMProfile(BaseModel):
    has_financial_impact: bool = True
    is_innovative: bool = False
    has_quantitative_metrics: bool = True
    resource_constrained: bool = False
    has_regulatory_blockers: bool = False
    rice_score: float = 0.0 # Reach * Impact * Confidence / Effort

class OKRProfile(BaseModel):
    deployment_frequency_low: bool = False
    lead_time_high: bool = False
    mttr_high: bool = False
    change_failure_rate_high: bool = False
    strategic_business_goal_active: bool = False
    quality_degradation: bool = False

class TradeoffProfile(BaseModel):
    is_core_business: bool = True
    time_to_market_critical: bool = False
    mature_saas_available: bool = False
    budget_constrained: bool = False
    long_term_maintenance_critical: bool = True

class PlatformProfile(BaseModel):
    team_size: int = 2
    multiple_stacks: bool = False
    high_compliance_needs: bool = False
    high_onboarding_frequency: bool = False

class SeniorEvalProfile(BaseModel):
    sys_design_score: float = 3.0
    coding_score: float = 3.0
    tradeoff_score: float = 3.0
    behavioral_score: float = 3.0
    comm_score: float = 3.0
    product_score: float = 3.0

class CulturalFitProfile(BaseModel):
    ownership_score: float = 3.0
    conflict_score: float = 3.0
    feedback_score: float = 3.0
    collaboration_score: float = 3.0
    transparency_score: float = 3.0
    learning_score: float = 3.0

class TeamStructureProfile(BaseModel):
    total_developers: int = 5
    current_model: str = "flat"
    regulatory_level: str = "low"
    platform_maturity: str = "none"

class ComplianceProfile(BaseModel):
    frameworks: List[str] = []
    required_region: str = "US"
    currency: str = "USD" # New: For localization
    availability_target: str = "99.9%"
    multi_region: bool = False # New: For DR architecture

class GDPRMetadata(BaseModel):
    personal_data: bool = False
    special_category: bool = False
    pseudonymized: bool = False
    anonymized: bool = False
    reidentification_risk: float = 0.0 # 0.0 to 1.0

class RetentionRule(BaseModel):
    category: str = "general" # e.g., 'marketing', 'aml', 'accounting'
    ttl_days: int = 365
    legal_basis: str = "consent" # e.g., 'legal_obligation', 'contract'

class DataLifecycle(BaseModel):
    policies: List[RetentionRule] = []
    crypto_shredding_enabled: bool = False
    purge_on_expiration: bool = True
    audit_proof_required: bool = True

class DPIARisk(BaseModel):
    description: str = ""
    likelihood: int = 1 # 1-5
    impact: int = 1 # 1-5
    score: int = 1 # Likelihood x Impact
    mitigation_strategy: str = ""
    residual_risk: int = 1

class DPIAAssessment(BaseModel):
    is_mandatory: bool = False
    triggers: List[str] = []
    risks: List[DPIARisk] = []
    overall_risk_level: str = "Low" # Low, Medium, High, Extreme
    dpo_approval_required: bool = False

class TransferAssessment(BaseModel):
    is_international: bool = False
    destination_country: str = "EU"
    adequacy_status: str = "Adequate" # Adequate, Conditional, Not Adequate
    legal_basis: str = "GDPR Art. 45" # SCCs, BCRs, Adequacy
    tia_required: bool = False
    tia_completed: bool = False
    supplementary_measures: List[str] = []
    jurisdictional_risk_level: str = "Low"

class ArchitectureSpec(BaseModel):
    pattern_id: str = ""
    components: List[Dict[str, Any]] = [] # Each component can now have 'gdpr' key with GDPRMetadata
    infrastructure: Dict[str, Any] = {}
    replicas: Dict[str, int] = {}
    enterprise_patterns: List[Dict[str, Any]] = []
    lifecycle: DataLifecycle = Field(default_factory=DataLifecycle)
    dpia_report: DPIAAssessment = Field(default_factory=DPIAAssessment)
    transfer_assessment: TransferAssessment = Field(default_factory=TransferAssessment)
    observability: Dict[str, Any] = {}
    reliability: Dict[str, Any] = {}
    tracing: Dict[str, Any] = {}
    chaos: Dict[str, Any] = {}
    deployment: Dict[str, Any] = {}
    gitops: Dict[str, Any] = {}
    supply_chain: Dict[str, Any] = {}
    iac: Dict[str, Any] = {}
    performance: Dict[str, Any] = {}
    profiling: Dict[str, Any] = {}
    db_optimization: Dict[str, Any] = {}
    frontend_perf: Dict[str, Any] = {}
    tech_debt: Dict[str, Any] = {}
    code_review: Dict[str, Any] = {}
    aff: Dict[str, Any] = {}
    scalability: Dict[str, Any] = {}
    tpm: Dict[str, Any] = {}
    okrs: Dict[str, Any] = {}
    tradeoff_analysis: Dict[str, Any] = {}
    platform_engineering: Dict[str, Any] = {}
    senior_evaluation: Dict[str, Any] = {}
    cultural_fit: Dict[str, Any] = {}
    team_structure: Dict[str, Any] = {}
    onboarding: Dict[str, Any] = {}
    unit_economics: Dict[str, Any] = {}
    ltv_dynamics: Dict[str, Any] = {}
    networking: Dict[str, Any] = { # New: Deep networking stack

        "vpc_cidr": "10.0.0.0/16",
        "subnets": [],
        "gateways": [],
        "security_groups": []
    }


class FinancialModel(BaseModel):
    cloud_costs: Dict[str, Any] = {}
    on_prem_costs: Dict[str, Any] = {}
    usage_breakdown: Dict[str, float] = {} # New: Egress, Storage, Compute
    npv: float = 0.0
    roi_months: int = 0
    scenarios: Dict[str, Any] = {}

class ComplianceEvidence(BaseModel):
    data_registry_updated: bool = False
    immutable_logs_enabled: bool = False
    encryption_verified: bool = False
    retention_enforced: bool = False
    incident_register_ready: bool = False
    dpo_review_status: str = "Pending" # Pending, Reviewed, Approved

class BdEGovernance(BaseModel):
    is_supervised_entity: bool = False
    board_approval_status: str = "Pending" # Pending, Approved, Rejected
    internal_control_robustness: float = 0.0 # 0.0 to 1.0
    operational_risk_mapping: bool = False
    incident_reporting_automated: bool = False
    change_management_integrity: bool = False

class SCAConfig(BaseModel):
    factors_enabled: List[str] = [] # Knowledge, Possession, Inherence
    dynamic_linking_active: bool = False
    authentication_channel: str = "Mobile App"
    biometrics_supported: bool = False

class TRAEngine(BaseModel):
    fraud_rate: float = 0.0
    thresholds: Dict[str, float] = {
        "50_eur": 0.13,
        "100_eur": 0.06,
        "250_eur": 0.01
    }
    is_real_time: bool = False
    audit_log_immutable: bool = False

class PSD2Compliance(BaseModel):
    sca_required: bool = False
    exemption_applied: str = "None" # None, Low Value, TRA, Trusted, Recurring
    tra_assessment: TRAEngine = Field(default_factory=TRAEngine)
    sca_config: SCAConfig = Field(default_factory=SCAConfig)
    rts_sca_status: str = "Pending"

class KYCConfig(BaseModel):
    biometrics_enabled: bool = False
    document_verification_automated: bool = False
    pep_sanctions_screening_realtime: bool = False
    liveness_detection: bool = False

class AMLMonitoringConfig(BaseModel):
    is_real_time: bool = False
    anomaly_detection_enabled: bool = False
    thresholds_configurable: bool = False
    case_management_integrated: bool = False

class AML_RBA_Model(BaseModel):
    geography_score: int = 0 # 0-5
    activity_score: int = 0
    product_risk: int = 0
    channel_risk: int = 0
    total_risk_score: float = 0.0
    risk_category: str = "Low" # Low, Medium, High

class AMLCompliance(BaseModel):
    is_in_scope: bool = False
    kyc_config: KYCConfig = Field(default_factory=KYCConfig)
    monitoring: AMLMonitoringConfig = Field(default_factory=AMLMonitoringConfig)
    rba_assessment: AML_RBA_Model = Field(default_factory=AML_RBA_Model)
    ubo_registry_immutable: bool = False
    sepblac_reporting_ready: bool = False
    retention_policy_years: int = 10

class InvestmentConfig(BaseModel):
    investor_classification_automated: bool = False
    knowledge_test_mandatory: bool = False
    suitability_test_structured: bool = False
    cooling_off_period_enforced: bool = False
    algorithmic_explainability: bool = False

class CryptoConfig(BaseModel):
    wallet_segregation: bool = False
    cold_storage_hsm: bool = False
    private_key_hardening: bool = False
    market_abuse_detection: bool = False
    mica_whitepaper_ready: bool = False

class InvestorRiskModel(BaseModel):
    knowledge_score: int = 0
    experience_years: int = 0
    loss_capacity_percent: float = 0.0
    risk_tolerance: str = "Low" # Low, Medium, High
    suitability_profile: str = "Conservative" # Conservative, Balanced, Growth, Speculative

class CNMVCompliance(BaseModel):
    is_in_scope: bool = False
    investment_type: str = "None" # Crowdfunding, Roboadvisor, Broker, Crypto, None
    investment_config: InvestmentConfig = Field(default_factory=InvestmentConfig)
    crypto_config: CryptoConfig = Field(default_factory=CryptoConfig)
    investor_risk: InvestorRiskModel = Field(default_factory=InvestorRiskModel)
    asset_segregation_verified: bool = False
    regulatory_logs_ready: bool = False

class DeveloperOnboardingProfile(BaseModel):
    ttfc_target_days: int = 3
    ttfp_target_days: int = 10
    onboarding_maturity: str = "Ad-hoc" # Ad-hoc, Structured, Data-Driven

class UnitEconomicsProfile(BaseModel):
    cac: float = 0.0 # Customer Acquisition Cost in EUR
    monthly_arpu: float = 0.0 # Average Revenue Per User/month
    gross_margin_pct: float = 70.0 # Gross Margin %
    monthly_churn_pct: float = 5.0 # Monthly churn rate %
    ltv: float = 0.0 # Calculated Lifetime Value
    payback_months: float = 0.0 # Months to recover CAC
    ltv_cac_ratio: float = 0.0 # The ratio investors examine
    business_model: str = "B2B SaaS" # B2C, B2B SMB, B2B Mid-Market, Enterprise

class LTVDynamicsProfile(BaseModel):
    nrr_pct: float = 100.0 # Net Revenue Retention %
    expansion_revenue_pct: float = 0.0 # Monthly expansion as % of starting
    contraction_revenue_pct: float = 0.0 # Monthly contraction as % of starting
    expansion_model: str = "none" # seat_based, usage_based, tiered, none
    churn_stage: str = "unknown" # early (<60d), mid (60-180d), late (>180d), unknown
    cohort_health: str = "unknown" # stabilizing, degrading, flat, unknown
    dynamic_ltv: float = 0.0 # LTV computed with dynamic churn + expansion

class GlobalState(BaseModel):
    # Layer 0: Original Input
    raw_input: Dict[str, Any] = {}
    
    # Layer 1: Normalized Requirements
    requirements: Dict[str, Any] = {}
    traffic_profile: TrafficProfile = Field(default_factory=TrafficProfile)
    data_profile: DataProfile = Field(default_factory=DataProfile)
    
    # Computed Metrics (Layer 2 pre-processing)
    runtime_metrics: Dict[str, Any] = {}

    # Plugin Results (Layer 2 — dynamic)
    pillar_results: Dict[str, Any] = {}
    
    tech_debt_profile: TechDebtProfile = Field(default_factory=TechDebtProfile)
    code_review_profile: CodeReviewProfile = Field(default_factory=CodeReviewProfile)
    arch_fitness_profile: ArchFitnessProfile = Field(default_factory=ArchFitnessProfile)
    scalability_profile: ScalabilityProfile = Field(default_factory=ScalabilityProfile)
    tpm_profile: TPMProfile = Field(default_factory=TPMProfile)
    okr_profile: OKRProfile = Field(default_factory=OKRProfile)
    tradeoff_profile: TradeoffProfile = Field(default_factory=TradeoffProfile)
    platform_profile: PlatformProfile = Field(default_factory=PlatformProfile)
    senior_eval_profile: SeniorEvalProfile = Field(default_factory=SeniorEvalProfile)
    cultural_fit_profile: CulturalFitProfile = Field(default_factory=CulturalFitProfile)
    team_structure_profile: TeamStructureProfile = Field(default_factory=TeamStructureProfile)
    onboarding_profile: DeveloperOnboardingProfile = Field(default_factory=DeveloperOnboardingProfile)
    unit_economics_profile: UnitEconomicsProfile = Field(default_factory=UnitEconomicsProfile)
    ltv_dynamics_profile: LTVDynamicsProfile = Field(default_factory=LTVDynamicsProfile)
    compliance_profile: ComplianceProfile = Field(default_factory=ComplianceProfile)
    
    # Layer 2: Architecture
    architecture: ArchitectureSpec = Field(default_factory=ArchitectureSpec)
    
    # Layer 3: Costs & Calculations
    costs: Dict[str, Any] = {}
    financial_model: FinancialModel = Field(default_factory=FinancialModel)
    
    # Layer 4: Visualization
    diagrams_paths: Dict[str, str] = {}
    
    # Layer 5: Risks & Final Validation
    risk_matrix: List[Dict[str, Any]] = []
    technical_audit: List[Dict[str, Any]] = [] # New: Detailed 2026 Audit
    evidence_vault: ComplianceEvidence = Field(default_factory=ComplianceEvidence)
    bde_governance: BdEGovernance = Field(default_factory=BdEGovernance)
    psd2_compliance: PSD2Compliance = Field(default_factory=PSD2Compliance)
    aml_compliance: AMLCompliance = Field(default_factory=AMLCompliance)
    cnmv_compliance: CNMVCompliance = Field(default_factory=CNMVCompliance)
    compliance_score: float = 0.0
    audit_ready_score: float = 0.0
    is_frozen: bool = False






    def freeze(self):
        self.is_frozen = True
