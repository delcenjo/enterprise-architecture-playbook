import os
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from typing import Dict, Any

class SmartTemplateEngine:
    def __init__(self, templates_dir: str = "templates"):
        # StrictUndefined garantiza que el pipeline falle (y no genere datos basura) 
        # si falta una variable, cumpliendo con la regla de arquitectura anti-errores.
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Filtros útiles para plantillas empresariales
        self.env.filters['currency'] = self._format_currency
        self.env.filters['percent'] = self._format_percent

    def _format_currency(self, value: float) -> str:
        return f"${value:,.2f}"

    def _format_percent(self, value: float) -> str:
        return f"{value * 100:.2f}%"

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Renderiza un template de Markdown. Nunca se inyectan variables sin definir.
        """
        template = self.env.get_template(template_name)
        return template.render(**context)
