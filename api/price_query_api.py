import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import DictCursor

app = FastAPI(title="AWS Pricing API", version="1.0.0")

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_NAME = os.environ.get("DB_NAME", "pricing")
DB_PORT = os.environ.get("DB_PORT", "5432")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
        port=DB_PORT
    )

class CostCalculationRequest(BaseModel):
    instance_type: str = "t3.medium"
    region: str = "eu-west-1"
    hours_per_month: int = 730
    operating_system: str = "Linux"

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/calculate")
async def calculate_cost(request: CostCalculationRequest):
    """
    Endpoint usado por la Capa 3 (Intelligence) para obtener costes reales
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=DictCursor)
        
        cur.execute("""
            SELECT price_per_hour, vcpus, memory_gb, raw_json, ingestion_timestamp
            FROM aws_pricing_current
            WHERE instance_type = %s 
              AND region_code = %s 
              AND operating_system = %s
              AND tenancy = 'Shared'
              AND is_current = TRUE
            LIMIT 1
        """, (request.instance_type, request.region, request.operating_system))
        
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not result:
            raise HTTPException(
                status_code=404, 
                detail=f"Price not found for {request.instance_type} in {request.region}"
            )
        
        price_per_hour = float(result['price_per_hour'])
        monthly_cost = price_per_hour * request.hours_per_month
        
        return {
            "instance_type": request.instance_type,
            "specs": {
                "vcpus": result['vcpus'], 
                "memory_gb": float(result['memory_gb']) if result['memory_gb'] else 0.0
            },
            "costs": {
                "hourly": round(price_per_hour, 6),
                "monthly": round(monthly_cost, 2),
                "yearly": round(monthly_cost * 12, 2)
            },
            "confidence": 1.0,  # Datos reales de AWS = confianza máxima
            "source": "aws_price_list_api",
            "last_updated": result['ingestion_timestamp'].isoformat() if result['ingestion_timestamp'] else 'Unknown'
        }
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
