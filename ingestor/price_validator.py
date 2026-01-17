from typing import Dict, List, Tuple
import logging

class ValidationResult:
    def __init__(self, is_valid: bool, errors: List[str], warnings: List[str]):
        self.is_valid = is_valid
        self.errors = errors
        self.warnings = warnings

class PriceValidator:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("PriceValidator")

    def validate(self, new_product_data: Dict, historical_price: float = None) -> ValidationResult:
        errors = []
        warnings = []
        
        price = new_product_data.get('price_per_hour', 0.0)
        sku = new_product_data.get('sku', 'UNKNOWN')
        
        # Regla 1: Ningún precio puede ser 0 (error de parsing o de AWS)
        if price <= 0.0:
            errors.append(f"Zero or negative price detected for SKU: {sku}")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
        
        # Regla 2: Variación máxima 50% respecto al histórico (si existe)
        if historical_price is not None and historical_price > 0.0:
            variation = abs(price - historical_price) / historical_price
            
            if variation > 0.5:  # Cambió más del 50%
                errors.append(
                    f"Price anomaly for {sku}: ${price} vs historical ${historical_price} ({variation:.0%} change)"
                )
            elif variation > 0.2:  # Cambió más del 20%
                warnings.append(
                    f"Significant price change for {sku} ({variation:.0%})"
                )
        
        # Regla 3: Precios máximos razonables para EC2 OnDemand comunes MVP
        if price > 500:  # $500/hora es $360.000/mes! Bastante sospechoso.
            errors.append(f"Suspiciously high price: ${price}/hour for {sku}")
        
        is_valid = len(errors) == 0
        if not is_valid:
            for e in errors: self.logger.error(e)
            for w in warnings: self.logger.warning(w)

        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )
