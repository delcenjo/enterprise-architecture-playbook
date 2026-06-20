import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
import markdown2
from typing import Dict, Any, List

class PDFBuilder:
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = templates_dir
        self.env = Environment(loader=FileSystemLoader(templates_dir))

    def build_pdf(self, client_name: str, project_name: str, sections: List[Dict[str, Any]]) -> bytes:
        """Convierte los bloques Markdown a HTML y genera el PDF con WeasyPrint."""
        
        rendered_sections = []
        for sec in sections:
            raw_md = sec.get("content", "")
            html_chunk = markdown2.markdown(raw_md, extras=["tables", "fenced-code-blocks"])
            rendered_sections.append({
                "title": sec.get("title", "Sección"),
                "html_content": html_chunk
            })

        template = self.env.get_template("master_dossier.html.j2")
        full_html = template.render(
            client_name=client_name,
            project_name=project_name,
            sections=rendered_sections
        )

        css_path = os.path.join(self.templates_dir, "pdf_style.css")

        pdf_bytes = HTML(string=full_html).write_pdf(
            stylesheets=[CSS(filename=css_path)]
        )
        
        return pdf_bytes
