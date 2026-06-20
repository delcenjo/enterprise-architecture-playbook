from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import httpx
import logging
from pydantic import BaseModel, Field, root_validator
from typing import Dict, Any, List, Optional
from workflow_manager import WorkflowManager
import asyncio
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Architecture Orchestrator", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INTELLIGENCE_URL = "http://intelligence:8001"
OUTPUT_GENERATOR_URL = "http://output_generator:8002"

wm = WorkflowManager()

class ProjectContext(BaseModel):
    company_type: str = "Enterprise" # Startup, Scale-up, Enterprise, Regulated
    industry: str = "General" # Fintech, Healthtech, SaaS, etc.
    countries_of_operation: List[str] = Field(default_factory=list) # ES, EU, US, etc.
    product_phase: str = "Scaling" # MVP, PMF, Scaling, Enterprise-grade

class CurrentArchitecture(BaseModel):
    architecture_type: str = "Monolith" # Monolith, Microservices, Serverless
    cloud_provider: str = "AWS" # AWS, GCP, Azure, On-prem
    tenancy_model: str = "Single-tenant" # Single-tenant, Multi-tenant
    primary_database: str = "PostgreSQL" # PostgreSQL, MySQL, Mongo, etc.
    messaging_system: str = "None" # Kafka, RabbitMQ, SQS, None
    observability_level: str = "Basic" # Basic, Intermediate, Advanced
    cicd_maturity: str = "Manual" # Manual, Semi-automated, GitOps

class ScaleAndLoad(BaseModel):
    monthly_active_users: int = 10000
    peak_concurrent_users: int = 500
    estimated_rps: float = 50.0
    current_p95_latency_ms: float = 500.0
    expected_mom_growth_pct: float = 5.0
    active_regions: int = 1
    target_sla: str = "99.9%" # 99%, 99.9%, 99.99%

class DataAndSensitivity(BaseModel):
    processes_pii: bool = False
    special_categories: bool = False # Health, Biometrics
    processes_payments: bool = False
    regulated_entity: bool = False # DORA, CNMV, BDE
    data_retention_years: float = 5.0
    cross_border_transfers: bool = False

class TeamAndOrganization(BaseModel):
    total_developers: int = 10
    total_sre_devops: int = 1
    has_platform_team: bool = False
    average_seniority: str = "Mid" # Junior, Mid, Senior
    deployment_frequency: str = "Weekly" # Daily, Weekly, Monthly
    approximate_mttr: str = "Hours" # Minutes, Hours, Days

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

class EnterpriseIntakeSchema(BaseModel):
    client_name: str
    project_name: str
    project_context: ProjectContext = Field(default_factory=ProjectContext)
    current_architecture: CurrentArchitecture = Field(default_factory=CurrentArchitecture)
    scale_and_load: ScaleAndLoad = Field(default_factory=ScaleAndLoad)
    data_and_sensitivity: DataAndSensitivity = Field(default_factory=DataAndSensitivity)
    team_and_organization: TeamAndOrganization = Field(default_factory=TeamAndOrganization)
    financials: Financials = Field(default_factory=Financials)
    user_objectives: UserObjectives = Field(default_factory=UserObjectives)
    advanced_overrides: Optional[str] = None

class ApprovalRequest(BaseModel):
    role: str # TECHNICAL, FINANCIAL, LEGAL, EDITORIAL
    approved: bool
    feedback: Optional[str] = None

@app.post("/workflow/start")
async def start_workflow(request: EnterpriseIntakeSchema, background_tasks: BackgroundTasks):
    workflow_id = wm.create_workflow(
        request.client_name, 
        request.project_name, 
        request.dict() # Passing the full structured schema as context
    )
    if not workflow_id:
        raise HTTPException(status_code=500, detail="Failed to initialize EventStream")
    
    background_tasks.add_task(ConsultingSaga(workflow_id).execute)
    return {"workflow_id": workflow_id, "status": "TECHNICAL_AUDIT"}

@app.get("/workflow/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    return wm.get_status(workflow_id)

@app.post("/workflow/{workflow_id}/approve")
async def approve_step(workflow_id: str, approval: ApprovalRequest, background_tasks: BackgroundTasks):
    status = wm.get_status(workflow_id)
    # Ejemplo: Gate 1 requiere aprobación TECHNICAL
    gate_mapping = {
        "PENDING_TECH_APPROVAL": "TECHNICAL",
        "PENDING_FINANCIAL_APPROVAL": "FINANCIAL",
        "PENDING_LEGAL_APPROVAL": "LEGAL",
        "PENDING_EDITORIAL_APPROVAL": "EDITORIAL"
    }
    
    expected_role = gate_mapping.get(status['current_status'])
    if not expected_role or approval.role != expected_role:
        raise HTTPException(status_code=400, detail=f"Unexpected approval role. Expected: {expected_role}")
    
    if not approval.approved:
        wm.update_state(workflow_id, "REJECTED", {"reason": approval.feedback, "role": approval.role})
        return {"status": "REJECTED"}

    wm.update_state(workflow_id, f"GATE_{approval.role}_PASSED", {"approver": approval.role})
    background_tasks.add_task(ConsultingSaga(workflow_id).resume)
    return {"status": "PROCEEDING"}

class ConsultingSaga:
    """
    Orquestador SAGA de Grado Industrial.
    Cada método es una fase que culmina en un Checkpoint Humano.
    """
    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id
        self.wm = wm

    async def execute(self):
        """Fase 1: Extracción Técnica y Verificación de Hechos."""
        try:
            status = self.wm.get_status(self.workflow_id)
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    f"{INTELLIGENCE_URL}/generate/section",
                    json={"document_type": "extraction", "context": status['context']}
                )
                resp.raise_for_status()
                data = resp.json()
                
                self.wm.update_state(self.workflow_id, "PENDING_TECH_APPROVAL", {
                    "extraction_facts": data['data'],
                    "confidence": data['metadata']['confidence']
                })
        except Exception as e:
            self.wm.update_state(self.workflow_id, "ERROR", {"phase": "TECHNICAL", "error": str(e)})

    async def resume(self):
        """Continúa la SAGA tras aprobación humana."""
        status = self.wm.get_status(self.workflow_id)
        current = status['current_status']
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            if current == "GATE_TECHNICAL_PASSED":
                # Fase 2: Cálculos Financieros Determinísticos
                resp = await client.post(
                    f"{INTELLIGENCE_URL}/generate/section",
                    json={"document_type": "cost_analysis", "context": status['context'], "facts": status['metadata']['extraction_facts']}
                )
                self.wm.update_state(self.workflow_id, "PENDING_FINANCIAL_APPROVAL", resp.json())
                
            elif current == "GATE_FINANCIAL_PASSED":
                # Fase 3: Compliance Mapping (DORA/GDPR)
                resp = await client.post(
                    f"{INTELLIGENCE_URL}/generate/section",
                    json={"document_type": "compliance_analysis", "context": status['context'], "facts": status['metadata']['extraction_facts']}
                )
                self.wm.update_state(self.workflow_id, "PENDING_LEGAL_APPROVAL", resp.json())

            elif current == "GATE_LEGAL_PASSED":
                # Fase 4: Editorial Synthesis & PDF Generation
                resp = await client.post(
                    f"{OUTPUT_GENERATOR_URL}/generate-dossier",
                    json={
                        "client_name": status['client_name'],
                        "project_name": status['project_name'],
                        "sections": status['metadata'].get('sections', [])
                    }
                )
                self.wm.update_state(self.workflow_id, "COMPLETED", {"dossier_ready": True})
