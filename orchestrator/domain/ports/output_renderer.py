"""
Port: OutputRenderer — Interface for generating deliverables (HTML, PDF, Excel).

Decouples report generation from specific templating and rendering libraries
(Jinja2, WeasyPrint, openpyxl, …).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class OutputRenderer(ABC):
    """Abstract contract for rendering analysis results into deliverables."""

    @abstractmethod
    def render_html(
        self,
        template_name: str,
        data: Dict[str, Any],
    ) -> str:
        """Render a named template with the given data and return HTML string.

        Parameters
        ----------
        template_name:
            Logical template identifier (e.g. ``'dossier_blueprint'``).
        data:
            Template context dictionary.

        Returns
        -------
        str
            Rendered HTML content.
        """
        ...

    @abstractmethod
    def render_pdf(
        self,
        html_content: str,
        output_path: str,
    ) -> Optional[str]:
        """Convert HTML content to a PDF file.

        Parameters
        ----------
        html_content:
            Rendered HTML string.
        output_path:
            Filesystem path where the PDF should be saved.

        Returns
        -------
        str or None
            Path to the generated PDF, or ``None`` if PDF rendering
            is unavailable.
        """
        ...
