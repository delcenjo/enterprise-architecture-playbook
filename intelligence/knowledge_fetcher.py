import os
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class KnowledgeFetcher:
    """
    Retrieves compliance rules and templates from the knowledge base based on tech stacks.
    """
    def __init__(self):
        self.db_url = f"host={os.getenv('DB_HOST', 'postgres')} " \
                      f"user={os.getenv('DB_USER', 'postgres')} " \
                      f"password={os.getenv('DB_PASSWORD', 'password')} " \
                      f"dbname={os.getenv('DB_NAME', 'pricing')} " \
                      f"port={os.getenv('DB_PORT', '5432')}"

    def get_compliance_for_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        """
        Busca artículos de compliance (DORA/RGPD) que apliquen a los tags del stack.
        """
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Usamos el operador @> para buscar en el JSONB de tags
                    query = "SELECT article_id, title, description, requirement_level FROM knowledge_compliance WHERE applies_to_tags ?| %s"
                    cur.execute(query, (tags,))
                    return cur.fetchall()
        except Exception as e:
            logger.error(f"Error fetching compliance from Capa 2: {e}")
            return []

    def get_template(self, template_key: str) -> Dict[str, Any]:
        """
        Recupera un template de documento de la Capa 2.
        """
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("SELECT content, version FROM knowledge_templates WHERE template_key = %s", (template_key,))
                    return cur.fetchone()
        except Exception as e:
            logger.error(f"Error fetching template from Capa 2: {e}")
            return None
