import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ValidationResult:
    def __init__(self, passed: bool, errors: List[str]):
        self.passed = passed
        self.errors = errors

class MultiLevelValidator:
    """
    Capa de Garantía de Calidad (Quality Gates) para atajar
    alucinaciones del LLM antes de que toquen el documento final.
    """
    
    def validate(self, original_factual_markdown: str, llm_enriched_markdown: str) -> ValidationResult:
        logger.info("Executing Multi-Level Validation...")
        errors = []
        
        factual_result = self._level3_factual_check(original_factual_markdown, llm_enriched_markdown)
        if not factual_result.passed:
            errors.extend(factual_result.errors)

        format_result = self._level2_format_check(llm_enriched_markdown)
        if not format_result.passed:
            errors.extend(format_result.errors)
            
        is_valid = len(errors) == 0
        if is_valid:
            logger.info("Multi-Level Validation PASSED.")
        else:
            logger.error(f"Multi-Level Validation FAILED: {errors}")
            
        return ValidationResult(passed=is_valid, errors=errors)

    def _extract_numbers(self, text: str) -> List[float]:
        """
        Extrae todos los números (enteros, decimales, porcentajes, divisas) del texto.
        """
        pattern = r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b'
        matches = re.findall(pattern, text)
        
        numbers = []
        for m in matches:
            cleaned = m.replace(',', '')
            try:
                numbers.append(float(cleaned))
            except ValueError:
                pass
        return numbers

    def _level3_factual_check(self, original: str, enriched: str) -> ValidationResult:
        """
        Comprueba que el LLM no ha inventado, modificado o borrado cifras financieras críticas.
        """
        original_nums = set(self._extract_numbers(original))
        enriched_nums = set(self._extract_numbers(enriched))
        
        missing_nums = original_nums - enriched_nums
        
        errors = []
        if missing_nums:
            errors.append(f"El LLM ha omitido cifras numéricas factuales: {missing_nums}")
            
        return ValidationResult(passed=len(errors) == 0, errors=errors)
        
    def _level2_format_check(self, text: str) -> ValidationResult:
        """
        Verifica que el layout esperado no se ha corrompido.
        """
        errors = []
        if "### Conclusión Ejecutiva" not in text:
            # Some LLMs might ignore the instruction to add this specific header
            errors.append("El LLM ignoró la directiva de formato y no incluyó '### Conclusión Ejecutiva'.")
            
        if "|" not in text and "-" not in text:
            errors.append("La tabla de Markdown generada por la plantilla ha sido destruida por el LLM.")
            
        return ValidationResult(passed=len(errors) == 0, errors=errors)
