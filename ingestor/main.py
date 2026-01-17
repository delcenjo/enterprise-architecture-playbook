import os
import psycopg2
from psycopg2.extras import Json
from datetime import datetime
import time
import logging

from aws_price_ingestor import AWSPriceIngestor
from price_validator import PriceValidator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

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

def fetch_historical_price(cursor, sku: str):
    cursor.execute("""
        SELECT price_per_hour FROM aws_pricing_current
        WHERE sku = %s AND is_current = TRUE
        LIMIT 1
    """, (sku,))
    res = cursor.fetchone()
    return float(res[0]) if res else None

def main():
    logger.info("Starting AWS Price Ingestion Pipeline...")
    
    # Wait for DB to be ready
    conn = None
    retries = 5
    while retries > 0:
        try:
            conn = get_db_connection()
            break
        except Exception as e:
            logger.warning(f"DB not ready yet, retrying... ({retries} left)")
            time.sleep(5)
            retries -= 1
            
    if not conn:
        logger.error("Could not connect to database. Exiting.")
        return

    ingestor = AWSPriceIngestor(region='us-east-1')
    validator = PriceValidator()
    
    # 1. Fetch from AWS
    logger.info("Fetching data from AWS...")
    ingestion_payload = ingestor.fetch_all_prices('AmazonEC2', 'EU (Ireland)')
    
    valid_products_to_insert = []
    
    # 2. Validate
    logger.info("Validating prices...")
    cursor = conn.cursor()
    for raw_product in ingestion_payload['data']:
        parsed_data = ingestor.parse_product(raw_product)
        
        hist_price = fetch_historical_price(cursor, parsed_data['sku'])
        validation = validator.validate(parsed_data, hist_price)
        
        if validation.is_valid:
            valid_products_to_insert.append(parsed_data)
        else:
            logger.error(f"Validation failed for SKU {parsed_data['sku']}. Not inserting.")
            
    # 3. Insert / Update Database
    logger.info(f"Inserting {len(valid_products_to_insert)} approved products into DB...")
    
    effective_date = datetime.utcnow().date()
    checksum = ingestion_payload['checksum']
    
    for pd in valid_products_to_insert:
        try:
            cursor.execute("""
                INSERT INTO aws_pricing_current
                (sku, service_code, region_code, instance_type, vcpus, memory_gb, 
                 operating_system, tenancy, price_per_hour, currency, 
                 effective_date, ingestion_timestamp, raw_json, checksum, is_current)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, TRUE)
                ON CONFLICT (sku) DO UPDATE SET
                    price_per_hour = EXCLUDED.price_per_hour,
                    effective_date = EXCLUDED.effective_date,
                    ingestion_timestamp = NOW(),
                    raw_json = EXCLUDED.raw_json,
                    checksum = EXCLUDED.checksum
            """, (
                pd['sku'], pd['service_code'], pd['region_code'], pd['instance_type'], 
                pd['vcpus'], pd['memory_gb'], pd['operating_system'], pd['tenancy'], 
                pd['price_per_hour'], pd['currency'], effective_date, Json(pd['raw_json']), checksum
            ))
        except Exception as e:
            logger.error(f"Error inserting SKU {pd['sku']}: {e}")
            conn.rollback()

    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Pipeline completed successfully.")

if __name__ == "__main__":
    main()
