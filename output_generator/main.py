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
    sections: List[Dict[str, Any]]

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/generate-dossier")
async def generate_dossier(request: DossierRequest):
    """Genera el PDF y los artefactos técnicos, y los devuelve empaquetados en un ZIP."""
    logger.info(f"Generating full dossier for {request.client_name}...")
    
    try:
        pdf_builder = PDFBuilder()
        pdf_bytes = pdf_builder.build_pdf(
            client_name=request.client_name,
            project_name=request.project_name,
            sections=request.sections
        )

        assets_builder = AssetsBuilder()
        zip_bytes = assets_builder.build_full_package(
            client_name=request.client_name,
            pdf_bytes=pdf_bytes,
            sections=request.sections
        )

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
