import os
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import uuid
from typing import Dict, Any, Optional, List
import json
import hashlib
from datetime import datetime

logger = logging.getLogger(__name__)

class EventStore:
    """
    Capa 4: Motor de Event Sourcing con Integridad Criptográfica.
    Implementa el "Immutable Audit Trail".
    """
    def __init__(self):
        self.db_url = f"host={os.getenv('DB_HOST', 'postgres')} " \
                      f"user={os.getenv('DB_USER', 'postgres')} " \
                      f"password={os.getenv('DB_PASSWORD', 'password')} " \
                      f"dbname={os.getenv('DB_NAME', 'pricing')} " \
                      f"port={os.getenv('DB_PORT', '5432')}"

    def _compute_checksum(self, payload: Dict[str, Any]) -> str:
        """SHA-256 de la representación canónica del JSON."""
        dumped = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(dumped.encode()).hexdigest()

    def append_event(self, aggregate_id: str, event_type: str, payload: Dict[str, Any], correlation_id: str = None, causation_id: str = None) -> bool:
        """Registra un evento inmutable con checksum."""
        checksum = self._compute_checksum(payload)
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """INSERT INTO events 
                           (aggregate_id, event_type, payload, checksum, correlation_id, causation_id) 
                           VALUES (%s, %s, %s, %s, %s, %s)""",
                        (aggregate_id, event_type, json.dumps(payload), checksum, correlation_id, causation_id)
                    )
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"EventStore Write Error: {e}")
            return False

    def get_events(self, aggregate_id: str) -> List[Dict[str, Any]]:
        """Recupera el stream completo de eventos para un agregado."""
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(
                        "SELECT * FROM events WHERE aggregate_id = %s ORDER BY sequence_number ASC",
                        (aggregate_id,)
                    )
                    events = cur.fetchall()
                    for ev in events:
                        actual_checksum = self._compute_checksum(ev['payload'])
                        if actual_checksum != ev['checksum']:
                            raise ValueError(f"CRITICAL: Event {ev['event_id']} integrity check failed!")
                    return events
        except Exception as e:
            logger.error(f"EventStore Read Error: {e}")
            return []

class WorkflowManager:
    """
    Capa 4: Orquestador de Estado basado en Eventos.
    Reconstruye el estado actual consultando el EventStore.
    """
    def __init__(self):
        self.event_store = EventStore()

    def create_workflow(self, client_name: str, project_name: str, context: Dict[str, Any]) -> str:
        workflow_id = str(uuid.uuid4())
        payload = {
            "client_name": client_name,
            "project_name": project_name,
            "context": context,
            "status": "CREATED"
        }
        if self.event_store.append_event(workflow_id, "WORKFLOW_CREATED", payload):
            return workflow_id
        return None

    def update_state(self, workflow_id: str, new_status: str, data: Dict[str, Any]):
        payload = {
            "to_status": new_status,
            "update_data": data,
            "timestamp": datetime.now().isoformat()
        }
        self.event_store.append_event(workflow_id, "STATE_TRANSITION", payload)

    def get_status(self, workflow_id: str) -> Dict[str, Any]:
        """Reconstruye el estado (Projection) a partir de los eventos."""
        events = self.event_store.get_events(workflow_id)
        if not events:
            return None
        
        state = {}
        for ev in events:
            if ev['event_type'] == "WORKFLOW_CREATED":
                state = ev['payload']
            elif ev['event_type'] == "STATE_TRANSITION":
                state["status"] = ev['payload']["to_status"]
                state.setdefault("metadata", {}).update(ev['payload']["update_data"])
        
        state["workflow_id"] = workflow_id
        state["current_status"] = state.get("status") 
        return state
