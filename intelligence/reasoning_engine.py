import os
import logging
from typing import Dict, Any
import litellm

logger = logging.getLogger(__name__)

# Default high-capability model; override via LLM_MODEL
DEFAULT_MODEL = os.environ.get("LLM_MODEL", "gpt-4o")

class SectionGenerator:
    """
    LLM reasoning layer. Transforms raw technical data into strategic business analysis.
    """
    def __init__(self, model_override: str = None):
        self.model = model_override or DEFAULT_MODEL
        self.use_mock = os.environ.get("OPENAI_API_KEY") in [None, "", "dummy_key_for_now"]

    def _call_llm(self, prompt: str) -> str:
        if self.use_mock:
            return "ANALYSIS PARTNER: Tras evaluar los estados financieros y el stack técnico, hemos identificado brechas críticas en el Tiering de redundancia que suponen un riesgo sistémico. Se recomienda ejecución inmediata de la Fase 1."

        try:
            response = litellm.completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM Error: {e}")
            return "ADVISORY ERROR: Fallo en la generación de narrativa estratégica. Consultar datos brutos de Capa 2."

    def generate_with_reasoning(self, raw_markdown: str, context: Dict[str, Any]) -> str:
        """
        Enriches a technical draft with strategic business reasoning via a two-pass LLM call.
        """
        logger.info(f"Escalating reasoning to {self.model} (Consulting Persona)...")
        
        reasoning_prompt = f"""
        Actúa como un Partner (Socio) de una consultora estratégica de primer nivel (McKinsey/Deloitte).
        Tu objetivo es transformar datos técnicos en un análisis de alto valor para un C-Level (CTO/CFO).
        
        BORRADOR TÉCNICO:
        {raw_markdown}
        
        CONTEXTO: Sector {context.get('sector')}, {context.get('company_size')} usuarios.
        
        TAREA:
        1. Identifica el 'Impacto en el Negocio' (no solo técnico).
        2. Detecta riesgos de cumplimiento (Compliance) basados en el stack detectado.
        3. Define una 'Visión Estratégica' que justifique la inversión.
        
        Sé directo, crítico y propositivo. Responde con un razonamiento ejecutivo.
        """
        
        reasoning = self._call_llm(reasoning_prompt)
        
        final_prompt = f"""
        Como Socio Consultor, integra este razonamiento estratégico en el documento base:
        
        DOCUMENTO BASE:
        {raw_markdown}
        
        RAZONAMIENTO ESTRATÉGICO:
        {reasoning}
        
        REGLAS DE ORO:
        - Mantén todos los datos numéricos y tablas intactos.
        - Añade una sección integral titulada `## Strategic Advisory & Executive Summary`.
        - Incluye una tabla de 'Riesgos vs Mitigación' basada en el análisis.
        - El tono debe ser formal, autoritario y de alto valor.
        """
        
        return self._call_llm(final_prompt)
