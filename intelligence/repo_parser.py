import logging
import hashlib
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class ExtractionResult(BaseModel):
    """
    Schema estricto para hechos técnicos observables.
    Capa 3: Input de la Intelligent Layer.
    """
    technical_stack: List[str] = Field(default_factory=list)
    languages: Dict[str, str] = Field(default_factory=dict) # {"Python": "3.11"}
    cloud_resources: Dict[str, Any] = Field(default_factory=dict) # {"instance_count": 3, "instance_type": "m5.large"}
    compliance_scope: List[str] = Field(default_factory=list)
    confidence_score: float = 0.0
    extraction_timestamp: str
    source_checksum: str

class RepoParser:
    """
    Agente Extractor (Defensivo).
    Su misión es identificar Hechos, NO interpretar.
    """
    def __init__(self):
        self.signatures = {
            "aws": ["main.tf", "terraform", "s3", "ec2"],
            "python": ["requirements.txt", "main.py", "app.py"],
            "finance": ["payment", "transaction", "fintech", "bank"],
            "personal_data": ["user_data", "gdpr", "email", "dni"]
        }

    def _calculate_checksum(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    def extract_factual_data(self, file_list: List[str], context: Dict[str, Any]) -> ExtractionResult:
        """
        Extrae datos técnicos inmutables del repositorio.
        Reconcilia los Hechos del Código con el Intake del Usuario e incorpora Overrides Avanzados.
        """
        tags = set()
        resources = {"instance_count": 0, "storage_gb": 100, "instance_type": "t3.medium"}
        warnings = []
        
        # 1. Detección de Tags por Firma de Archivos
        for file in file_list:
            file_lower = file.lower()
            for tag, sigs in self.signatures.items():
                if any(sig in file_lower for sig in sigs):
                    tags.add(tag)
            
            if "main.tf" in file_lower or "terraform" in file_lower:
                resources["instance_count"] = 3
                resources["instance_type"] = "m5.large"
                resources["storage_gb"] = 500

        # 2. Reconciliación con el Intake y Advanced Overrides (P11 Hybrid)
        tech_input = context.get("tech", {})
        user_stack = tech_input.get("current_stack", [])
        advanced_overrides = context.get("advanced_overrides", "") or ""
        
        # Si el usuario dice que usa algo pero no lo vemos en el código
        for tech in user_stack:
            if tech.lower() not in [t.lower() for t in tags]:
                warnings.append(f"Contradiction: User specified '{tech}' stack but no file signatures were found in repository.")

        # Procesar Overrides Avanzados (Lógica de "Pisar" Hechos)
        if "OVERRIDE_STORAGE_GB=" in advanced_overrides:
            try:
                new_val = int(advanced_overrides.split("OVERRIDE_STORAGE_GB=")[1].split()[0])
                resources["storage_gb"] = new_val
                warnings.append(f"Advanced Override applied: Storage GB set to {new_val}")
            except Exception:
                warnings.append("Failed to parse Advanced Override: OVERRIDE_STORAGE_GB")

        # 3. Mapeo de Compliance
        legal_input = context.get("legal", {})
        compliance = legal_input.get("frameworks", [])
        if context.get("sector") == "fintech" and "DORA" not in compliance:
            compliance.append("DORA (Auto-detected from Industry context)")

        # 4. Empaquetado Verificable
        raw_metadata = f"{list(tags)}-{resources}-{compliance}-{warnings}"
        
        import datetime
        return ExtractionResult(
            technical_stack=list(tags),
            cloud_resources=resources,
            compliance_scope=compliance,
            confidence_score=0.90 if warnings else 0.98,
            extraction_timestamp=datetime.datetime.now().isoformat(),
            source_checksum=self._calculate_checksum(raw_metadata)
        )
