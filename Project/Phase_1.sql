/*CREATE EXTENSION IF NOT EXISTS "uuid-ossp";*/

-- Runs table
CREATE TABLE IF NOT EXISTS runs (
  run_id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  status TEXT NOT NULL CHECK (status IN ('INGESTED','ANALYZED','FAILED')),
  jd_hash TEXT NOT NULL,
  resume_hash TEXT NOT NULL
);

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
  doc_id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
  run_id UUID NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  doc_type TEXT NOT NULL CHECK (doc_type IN ('JD','RESUME')),
  file_name TEXT,
  mime_type TEXT,
  text_content TEXT NOT NULL,
  sha256_hash TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Resume versions (stub for later)
CREATE TABLE IF NOT EXISTS resume_versions (
  version_id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
  base_run_id UUID NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  version_name TEXT NOT NULL CHECK (version_name IN ('v1','v2','v3')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Helpful index
CREATE INDEX IF NOT EXISTS idx_documents_run_id ON documents(run_id);


/*To drop the tables
DROP TABLES <table name>*/

/*To create a new schema
CREATE SCHEMA <schema_name> */

/*Used to show the which schema is using by default
SHOW search_path;*/

/*If we need to change it to the another path we can change it
SET search_path TO resume;
SHOW search_path;*/

