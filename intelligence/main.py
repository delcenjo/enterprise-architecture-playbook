from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from workflow_engine import DocumentOrchestrator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Intelligence Service (Document Forge)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationRequest(BaseModel):
    document_type: str = "cost_analysis"
    context: Dict[str, Any]
    files: Optional[List[str]] = []

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/generate/section")
async def generate_section(request: GenerationRequest):
    """
    Recibe la petición de generar una sección de un documento o el documento íntegro.
    """
    logger.info(f"Received generation request for type {request.document_type}")
    
    orchestrator = DocumentOrchestrator()
    
    if request.document_type == "cost_analysis":
        try:
            block = orchestrator.generate_cost_analysis_section(request.context)
            # ... (rest of the block)
            return {
                "status": "APPROVED",
                "section_id": block.section_id,
                "content": block.content,
                "metadata": {**block.metadata, "confidence": block.confidence, "sources": block.sources}
            }
        except Exception as e:
            logger.error(f"Failed to generate section: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    elif request.document_type == "compliance_analysis":
        try:
            block = orchestrator.generate_compliance_section(request.files, request.context)
            return {
                "status": "APPROVED",
                "section_id": block.section_id,
                "content": block.content,
                "metadata": {**block.metadata, "confidence": block.confidence, "sources": block.sources}
            }
        except Exception as e:
            logger.error(f"Failed to generate compliance section: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    elif request.document_type == "extraction":
        try:
            # Fact extraction doesn't produce Markdown, but structured JSON Facts
            files = request.context.get("repo_files", ["main.tf"])
            result = orchestrator.extract_facts(files, request.context)
            return {
                "status": "APPROVED",
                "data": result.dict(),
                "metadata": {
                    "confidence": result.confidence_score,
                    "checksum": result.source_checksum
                }
            }
        except Exception as e:
            logger.error(f"Factual extraction failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported document type: {request.document_type}")

