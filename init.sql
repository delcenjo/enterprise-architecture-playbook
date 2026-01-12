-- Tabla principal de precios (siempre versión actual)
CREATE TABLE IF NOT EXISTS aws_pricing_current (
    sku VARCHAR(100) PRIMARY KEY,  -- Ej: "RHT6XV3G29E4GX8B"
    service_code VARCHAR(50) NOT NULL,  -- "AmazonEC2"
    region_code VARCHAR(50) NOT NULL,   -- "eu-west-1"
    instance_type VARCHAR(50),          -- "t3.medium"
    vcpus INTEGER,
    memory_gb DECIMAL(10,2),
    operating_system VARCHAR(50),       -- "Linux", "Windows"
    tenancy VARCHAR(50),                -- "Shared", "Dedicated"
    price_per_hour DECIMAL(10,6) NOT NULL,
    currency CHAR(3) DEFAULT 'USD',
    effective_date DATE NOT NULL,
    ingestion_timestamp TIMESTAMP DEFAULT NOW(),
    raw_json JSONB NOT NULL,            -- Datos completos por si acaso
    checksum VARCHAR(64) NOT NULL,
    is_current BOOLEAN DEFAULT TRUE
);

-- Índices para consultas rápidas del sistema
CREATE INDEX IF NOT EXISTS idx_aws_pricing_lookup ON aws_pricing_current(
    service_code, region_code, instance_type, operating_system, is_current
);

-- Tabla histórica (time-series) para análisis de tendencias
CREATE TABLE IF NOT EXISTS aws_pricing_history (
    id BIGSERIAL PRIMARY KEY,
    sku VARCHAR(100) NOT NULL,
    price_per_hour DECIMAL(10,6) NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT NOW(),
    change_reason VARCHAR(255)  -- "AWS price drop", "New instance type", etc
);

-- Trigger: Cuando cambia un precio, guardar en histórico
CREATE OR REPLACE FUNCTION log_price_change()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.price_per_hour IS DISTINCT FROM NEW.price_per_hour THEN
        INSERT INTO aws_pricing_history (sku, price_per_hour, recorded_at, change_reason)
        VALUES (NEW.sku, OLD.price_per_hour, NOW(), 'Price updated');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_log_price_change ON aws_pricing_current;
CREATE TRIGGER trigger_log_price_change
    BEFORE UPDATE ON aws_pricing_current
    FOR EACH ROW
    EXECUTE FUNCTION log_price_change();
-- ==========================================
-- Capa 2: Knowledge Base (Compliance & Docs)
-- ==========================================

CREATE TABLE IF NOT EXISTS knowledge_compliance (
    id SERIAL PRIMARY KEY,
    article_id VARCHAR(50) NOT NULL UNIQUE, -- Ej: "DORA_ART_12"
    title VARCHAR(255) NOT NULL,
    description TEXT,
    applies_to_tags JSONB,                   -- Ej: ["cloud", "fintech", "payment_gateway"]
    requirement_level VARCHAR(20) DEFAULT 'MANDATORY', 
    regulatory_url TEXT
);

CREATE TABLE IF NOT EXISTS knowledge_templates (
    id SERIAL PRIMARY KEY,
    template_key VARCHAR(100) NOT NULL UNIQUE, -- Ej: "CONTRACT_SLA_V1"
    version VARCHAR(20) DEFAULT '1.0',
    content TEXT NOT NULL,
    category VARCHAR(50) -- "contract", "roadmap", "policy"
);

-- ==========================================
-- Capa 4: Workflow Orchestration & Event Store
-- ==========================================

CREATE TABLE IF NOT EXISTS workflow_state (
    workflow_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_name VARCHAR(255) NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    current_status VARCHAR(50) NOT NULL DEFAULT 'CREATED', -- EXTRACTING, REASONING, PENDING_HUMAN, COMPLETED
    metadata JSONB, -- Contexto actual del workflow
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS event_store (
    id BIGSERIAL PRIMARY KEY,
    workflow_id UUID NOT NULL REFERENCES workflow_state(workflow_id),
    event_type VARCHAR(100) NOT NULL, -- "STATE_TRANSITION", "ANALYSIS_RESULT", "HUMAN_APPROVAL"
    payload JSONB NOT NULL,
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- Datos iniciales de ejemplo para Capa 2
INSERT INTO knowledge_compliance (article_id, title, description, applies_to_tags)
VALUES 
('DORA_L1_ICT_RISK', 'DORA: Gestion de Riesgos TIC', 'Requisitos especificos para la gestion de riesgos de terceros en la nube.', '["aws", "cloud", "finance"]'),
('RGPD_ART_32', 'RGPD: Seguridad del Tratamiento', 'Medidas tecnicas para garantizar la proteccion de datos personales.', '["storage", "database", "personal_data"]')
ON CONFLICT (article_id) DO NOTHING;

INSERT INTO knowledge_templates (template_key, content, category)
VALUES 
('ROADMAP_18M_BASE', 'Timeline de 18 meses con hitos tecnologicos y de compliance.', 'roadmap'),
('SLA_CLOUD_STANDARD', 'Acuerdo de nivel de servicio estandar para despliegues AWS.', 'contract')
ON CONFLICT (template_key) DO NOTHING;
