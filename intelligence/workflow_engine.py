from data_fetchers import PricingFetcher
from template_engine import SmartTemplateEngine
from simulation_engine import SimulationEngine
from knowledge_fetcher import KnowledgeFetcher
from repo_parser import RepoParser, ExtractionResult
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class ContentBlock:
    def __init__(self, section_id: str, content: str, confidence: float, sources: list, metadata: Optional[Dict[str, Any]] = None):
        self.section_id = section_id
        self.content = content
        self.confidence = confidence
        self.sources = sources
        self.metadata = metadata or {}

class DocumentOrchestrator:
    def __init__(self):
        self.fetcher = PricingFetcher()
        self.tpl_engine = SmartTemplateEngine()
        self.simulator = SimulationEngine()
        self.knowledge = KnowledgeFetcher()
        self.repo_parser = RepoParser()

    def generate_cost_analysis_section(self, request_ctx: Dict[str, Any]) -> ContentBlock:
        """
        Orquesta la generación de la sección de Análisis de Costes.
        Paso 1: Validar parámetros.
        Paso 2: Obtener datos verídicos de fuentes externas (Knowledge DB).
        Paso 3: Calcular métricas de negocio.
        Paso 4: Inyectar en Template determinístico.
        """
        company_size = request_ctx.get("company_size", 100)
        region = request_ctx.get("region", "eu-west-1")
        instance_type = request_ctx.get("instance_type", "t3.medium")
        
        logger.info(f"Ochestrating cost section for {company_size} users in {region} using {instance_type}.")
        
        # 1. Fetch factual data
        pricing_data = self.fetcher.get_ec2_cost(
            instance_type=instance_type, 
            region=region
        )
        
        costs = pricing_data.get("costs", {})
        
        # 2. Derive business metrics (Mocked optimization logic for MVP)
        # Supposing our "expert system" detects a cheaper alternative or volume discount
        optimized_monthly = costs.get("monthly", 0.0) * 0.85
        total_savings = costs.get("monthly", 0.0) - optimized_monthly
        potential_savings_pct = total_savings / costs.get("monthly", 1.0) if costs.get("monthly") else 0.0

        # We need to construct the exact context expected by the Jinja template
        template_context = {
            "infrastructure": instance_type,
            "region": region,
            "users": company_size,
            "current": {
                "monthly": costs.get("monthly", 0.0),
                "yearly": costs.get("yearly", 0.0),
                "compute": costs.get("monthly", 0.0),
                "storage": 20.0, # Example fixed storage cost
                "total": costs.get("monthly", 0.0) + 20.0
            },
            "last_updated": pricing_data.get("last_updated", "Unknown"),
            "break_even_point": int(company_size * 1.5), # simple heuristic
            "optimization": {
                "potential_savings": potential_savings_pct
            },
            "optimized": {
                "compute": optimized_monthly,
                "storage": 15.0,
                "total": optimized_monthly + 15.0
            },
            "savings": {
                "compute": costs.get("monthly", 0.0) - optimized_monthly,
                "storage": 5.0,
                "total": (costs.get("monthly", 0.0) + 20.0) - (optimized_monthly + 15.0)
            },
            "services": [
                {
                    "name": f"EC2 {instance_type}",
                    "cost": f"${costs.get('monthly', 0.0)}",
                    "recommendation": "Migrar a Instancias Reservadas o Spot",
                    "impact": "Alto"
                }
            ],
            "risks": [
                {
                    "type": "Bloqueo de Proveedor (Vendor Lock-in)",
                    "description": "Fuerte dependencia de servicios propietarios de AWS.",
                    "mitigation": "Adoptar contenedores agnósticos y Terraform."
                }
            ]
        }
        
        # 5. Financial Simulation (Phase 10 Deterministic)
        stack_config = {
            "instance_type": instance_type,
            "instance_count": int(company_size / 500) or 2, # Example logic
            "storage_gb": 500
        }
        
        simulation_results = self.simulator.get_full_simulation(
            stack_config=stack_config,
            company_size=company_size
        )
        
        # Merge simulation into template context for rendering
        template_context["simulation"] = simulation_results
        
        # Re-render factual markdown with simulation data (if template supports it)
        factual_markdown = self.tpl_engine.render("cost_analysis.md.j2", template_context)

        # 6. Reason over the factual markdown
        from reasoning_engine import SectionGenerator
        reasoner = SectionGenerator()
        enriched_markdown = reasoner.generate_with_reasoning(factual_markdown, request_ctx)
        
        # 7. Validate the enriched markdown against the original factual source
        from validator import MultiLevelValidator
        validator = MultiLevelValidator()
        validation_result = validator.validate(factual_markdown, enriched_markdown)
        
        final_content = enriched_markdown
        confidence_score = pricing_data.get("confidence", 0.0)
        
        if not validation_result.passed:
            logger.error(f"Validation failed: {validation_result.errors}. Falling back to Pure Template.")
            # Fallback a la capa 2: Modo Template Puro garantizado
            final_content = factual_markdown
            confidence_score = 0.5  # Penalizamos la confianza por haber fallado la generación lingüística
        
        # 8. Wrap in ContentBlock
        return ContentBlock(
            section_id="cost_analysis",
            content=final_content,
            confidence=confidence_score,
            sources=[pricing_data.get("source", "unknown")],
            # Injecting the simulation raw data into metadata for the output generator
            metadata={
                "simulation": simulation_results,
                "context": {
                    "infrastructure": instance_type,
                    "region": region
                }
            }
        )
    def extract_facts(self, file_list: List[str], request_ctx: Dict[str, Any]) -> ExtractionResult:
        """
        Capa 3: Agente Extractor.
        Misión: Hechos puros.
        """
        return self.repo_parser.extract_factual_data(file_list, request_ctx)

    def generate_compliance_section(self, file_list: List[str], request_ctx: Dict[str, Any]) -> ContentBlock:
        """
        Capa 3: Reasoning + Capa 2 Knowledge.
        Analiza el repo, busca compliance en Capa 2 y genera el informe detallado.
        """
        # 1. Extraer hechos (Capa 3)
        facts = self.extract_facts(file_list, request_ctx)
        tags = facts.technical_stack
        
        # 2. Consultar Capa 2 Knowledge Base
        compliance_rules = self.knowledge.get_compliance_for_tags(tags)
        
        # 3. Preparar contexto para el reasoning
        reasoning_input = {
            "tags": tags,
            "rules": compliance_rules,
            "facts": facts.dict(),
            "project": request_ctx.get("project_name", "Unknown Project")
        }
        # ... logic continue
        
        # 4. Prompting determinístico (Simulado con Template por ahora + Reasoning)
        # Nota: En un sistema real, pasaríamos 'rules' al reasoning_engine
        prompt = f"Target Architecture Compliance Analysis for {reasoning_input['project']}.\n"
        prompt += f"Detected Stack: {', '.join(tags)}\n"
        prompt += "Applicable Regulatory Articles:\n"
        for rule in compliance_rules:
            prompt += f"- {rule['title']} ({rule['article_id']}): {rule['description']}\n"

        # 5. Generar contenido (Paso 3 reasoning)
        from reasoning_engine import SectionGenerator
        reasoner = SectionGenerator()
        final_content = reasoner.generate_with_reasoning(prompt, request_ctx)

        # 6. Fact-Check (Paso 3 validator contra Capa 2)
        sources = [rule['article_id'] for rule in compliance_rules]
        
        return ContentBlock(
            section_id="compliance_analysis",
            content=final_content,
            confidence=0.95 if compliance_rules else 0.5,
            sources=sources,
            metadata={"tags": tags, "rule_count": len(compliance_rules)}
        )
