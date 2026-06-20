import os
import json
import logging
import asyncio
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from jinja2 import Environment, FileSystemLoader
from global_state import GlobalState
from dotenv import load_dotenv

# Optional Providers
try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    from weasyprint import HTML
    HAS_WEASYPRINT = True
except ImportError:
    HAS_WEASYPRINT = False

load_dotenv()

logger = logging.getLogger("Layer6_NarrativeEngine")
logging.basicConfig(level=logging.INFO)

class NarrativeEngine:
    def __init__(self, state: GlobalState):
        self.state = state
        self.assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        self.cache_dir = os.path.join(os.path.dirname(__file__), "..", ".cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        self.env = Environment(loader=FileSystemLoader(self.assets_dir))
        self.env.filters['format_currency'] = lambda v: f"{float(v):,.2f}"
        
        # Configuration
        self.provider = os.getenv("PREMIUM_LLM_PROVIDER", "mock").lower()
        self.cache_enabled = os.getenv("ENABLE_NARRATIVE_CACHE", "true").lower() == "true"

    async def generate_premium_dossier(self) -> Dict[str, str]:
        """
        Generates the institutional-grade deliverable (HTML + PDF) using Hybrid LLM Narrative.
        """
        if not self.state.is_frozen:
            raise ValueError("State must be FROZEN before generating report.")

        logger.info(f"Forging Premium Dossier using Hybrid Intelligence ({self.provider})...")

        # 1. Generate Intelligent Narratives (API or Fallback)
        narratives = await self._get_intelligent_narratives()

        # 2. Template Preparation
        template_data = self._prepare_template_data(narratives)

        # 3. Render and Save
        template = self.env.get_template("dossier_blueprint.html")
        html_content = template.render(**template_data)
        
        html_path = os.path.join(self.assets_dir, "premium_report.html")
        with open(html_path, 'w') as f:
            f.write(html_content)

        pdf_path = os.path.join(self.assets_dir, "premium_report.pdf")
        if HAS_WEASYPRINT:
            logger.info("Exporting High-Res PDF (300dpi)...")
            HTML(string=html_content, base_url=self.assets_dir).write_pdf(pdf_path)
        else:
            pdf_path = None

        return {"html": html_path, "pdf": pdf_path}

    async def _get_intelligent_narratives(self) -> Dict[str, str]:
        """
        Orchestrates LLM calls with caching.
        """
        # Create unique hash for current state to check cache
        state_json = self.state.model_dump_json()
        cache_key = hashlib.sha256(state_json.encode()).hexdigest()
        cache_file = os.path.join(self.cache_dir, f"narrative_{cache_key}.json")

        if self.cache_enabled and os.path.exists(cache_file):
            logger.info("Reusing cached narrative from .cache/")
            with open(cache_file, 'r') as f:
                return json.load(f)

        # Generate fresh narrative
        narratives = await self._call_llm_api()
        
        if self.cache_enabled:
            with open(cache_file, 'w') as f:
                json.dump(narratives, f, indent=2)
        
        return narratives

    async def _call_llm_api(self) -> Dict[str, str]:
        """
        Multi-provider LLM connector.
        """
        summary_data = self._get_minimal_state_summary()
        prompt = self._build_executive_prompt(summary_data)
        
        try:
            if self.provider == "claude" and HAS_ANTHROPIC and os.getenv("ANTHROPIC_API_KEY"):
                return await self._call_claude(prompt)
            elif self.provider == "gemini" and HAS_GEMINI and os.getenv("GEMINI_API_KEY"):
                return await self._call_gemini(prompt)
            elif self.provider == "openai" and HAS_OPENAI and os.getenv("OPENAI_API_KEY"):
                return await self._call_openai(prompt)
        except Exception as e:
            logger.error(f"Premium LLM Call Failed ({self.provider}): {e}")
            logger.info("Falling back to Deterministic Template Narrative...")

        return self._generate_fallback_narrative()

    def _get_minimal_state_summary(self) -> str:
        """
        Extracts only the critical metrics to save tokens and prevent bias.
        """
        return json.dumps({
            "business": self.state.raw_input.get("business_type"),
            "traffic": self.state.traffic_profile.model_dump(),
            "financials": {
                "npv": self.state.financial_model.npv,
                "roi": self.state.financial_model.roi_months,
                "monthly_tco": self.state.costs.get("total_monthly")
            },
            "compliance": self.state.compliance_score,
            "architecture_pattern": self.state.architecture.pattern_id
        }, indent=2)

    def _build_executive_prompt(self, summary_json: str) -> str:
        return f"""
YOU ARE A SENIOR TECHNOLOGY CONSULTANT AT A TOP-TIER FIRM (MCKINSEY/GARTNER).
YOUR TASK: Generate a professional executive narrative for an Architecture Dossier.

STRICT RULES:
1. USE THE EXACT DATA PROVIDED. DO NOT INVENT NUMBERS.
2. TONE: Persuasive, professional, board-ready.
3. OUTPUT FORMAT: JSON with 'executive' and 'roadmap' keys.

DATA SOURCES (FROZEN STATE):
{summary_json}

INSTRUCTIONS:
- 'executive': Summarize the strategic value of this architecture. Mention specific ROI and Compliance metrics.
- 'roadmap': High-level next steps for implementation.
"""

    async def _call_claude(self, prompt: str) -> Dict[str, str]:
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2000,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )
        # Parse text into dict (simplified for the demo)
        return self._manual_parse_llm_output(message.content[0].text)

    async def _call_gemini(self, prompt: str) -> Dict[str, str]:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        return self._manual_parse_llm_output(response.text)

    async def _call_openai(self, prompt: str) -> Dict[str, str]:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return self._manual_parse_llm_output(response.choices[0].message.content)

    def _manual_parse_llm_output(self, text: str) -> Dict[str, str]:
        try:
            # Look for JSON structure in text
            start = text.find('{')
            end = text.rfind('}') + 1
            return json.loads(text[start:end])
        except:
            return {
                "executive": "Strategic review pending API validation.",
                "roadmap": "Roadmap pending technical verification."
            }

    def _generate_fallback_narrative(self) -> Dict[str, str]:
        return {
            "executive": f"Based on the deterministic audit, the {self.state.raw_input.get('business_type')} infrastructure is optimized for high-availability. The projected NPV remains positive at ${self.state.financial_model.npv:,.2f}.",
            "roadmap": "Immediate actions include VPC provisioning and compliance audit trail initialization."
        }

    def _prepare_template_data(self, narratives: Dict[str, str]) -> Dict[str, Any]:
        """
        Maps GlobalState to the template structure with V3 Transparency.
        """
        raw_reqs = self.state.costs.get("raw_requirements", {})
        resource_breakdown = self.state.costs.get("resource_breakdown", {})
        provider_comparison = self.state.costs.get("provider_comparison", {})
        currency = self.state.costs.get("currency", "USD")
        currency_symbol = self.state.costs.get("currency_symbol", "$")
        
        audit_table = [
            {"domain": "Performance Scale", "input": f"{self.state.raw_input.get('expected_users_year1'):,} users", "profile": f"{raw_reqs.get('compute', {}).get('vcpu', 0):.1f} vCPUs Required"},
            {"domain": "Network Throughput", "input": "Standard Payload", "profile": f"{raw_reqs.get('networking', {}).get('egress_gb', 0):.2f} GB/mo Egress"},
            {"domain": "Storage Performance", "input": "High IOPS", "profile": f"{raw_reqs.get('storage', {}).get('iops', 0):,.0f} IOPS Provisioned"}
        ]
        
        # Prepare Clean BOM
        clean_bom = []
        for comp in self.state.architecture.components:
            clean_bom.append({
                "name": comp['name'],
                "type": comp.get('type', 'Service'),
                "size": comp.get('role', 'Standard').upper(),
                "cost": comp.get('monthly_cost_est', 0.0)
            })

        return {
            "title": f"Institutional Strategy - {self.state.raw_input.get('business_type', 'Enterprise')}",
            "b_type": self.state.raw_input.get("business_type", "SaaS").upper(),
            "region": self.state.compliance_profile.required_region,
            "currency": currency,
            "currency_symbol": currency_symbol,
            "provider_comparison": provider_comparison,
            "npv": self.state.financial_model.npv,
            "roi_months": self.state.financial_model.roi_months,
            "compliance_score": int(self.state.compliance_score),
            "executive_narrative": narratives.get('executive', "Executive analysis generated with deterministic engine integrity."),
            "audit_table": audit_table,
            "resource_breakdown": resource_breakdown,
            "raw_reqs": raw_reqs,
            "architecture_pattern": self.state.architecture.pattern_id,
            "bom": clean_bom,
            "total_monthly": self.state.costs.get("total_monthly", 0.0),
            "risks": self.state.risk_matrix,
            "technical_audit": self.state.technical_audit,
            "risk_heatmap": self.state.diagrams_paths.get("risk_heatmap"),
            "enterprise_patterns": self.state.architecture.enterprise_patterns,
            "tradeoff_matrix": self._load_tradeoff_matrix(),
            "raw_input_json": json.dumps(self.state.raw_input, indent=2),
            "integrity_seal": self.state.costs.get("state_integrity_seal", "N/A"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def _load_tradeoff_matrix(self) -> Dict:
        path = os.path.join(os.path.dirname(__file__), "..", "knowledge", "patterns", "tradeoff_matrix.json")
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {}

if __name__ == "__main__":
    pass
