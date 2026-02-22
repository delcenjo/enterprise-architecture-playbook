from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, List
import io
import logging

from pdf_builder import PDFBuilder
from assets_builder import AssetsBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Output Layer (Deliverables)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DossierRequest(BaseModel):
    client_name: str = "Enterprise Corp"
    project_name: str = "Cloud Transformation Strategy"
    # This models the "ContentBlocks" we compiled in Phase 3
    sections: List[Dict[str, Any]]

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/generate-dossier")
async def generate_dossier(request: DossierRequest):
    """
    Recibe el contenido estructurado y aprobado (los Markdown)
    y lo empaqueta todo en un archivo ZIP con los 3 entregables clave.
    """
    logger.info(f"Generating full dossier for {request.client_name}...")
    
    try:
        # 1. Compilar el Documento Maestro (PDF 30-50 pages style)
        pdf_builder = PDFBuilder()
        pdf_bytes = pdf_builder.build_pdf(
            client_name=request.client_name,
            project_name=request.project_name,
            sections=request.sections
        )
        
        # 2. Compilar Artefactos Técnicos y Dashboard interactivo (ZIP)
        assets_builder = AssetsBuilder()
        zip_bytes = assets_builder.build_full_package(
            client_name=request.client_name,
            pdf_bytes=pdf_bytes,
            sections=request.sections
        )
        
        # Stream the zip back
        zip_io = io.BytesIO(zip_bytes)
        return StreamingResponse(
            zip_io,
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename=Consulting_Package_{request.client_name.replace(' ', '_')}.zip"
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating dossier: {e}")
        raise HTTPException(status_code=500, detail=str(e))
