/*CREATE TABLE IF NOT EXISTS resume.chunks (
  chunk_id TEXT PRIMARY KEY,
  run_id UUID NOT NULL REFERENCES resume.runs(run_id) ON DELETE CASCADE,
  source TEXT NOT NULL CHECK (source IN ('JD','RESUME','RUBRIC')),
  section TEXT NOT NULL,
  start_char INT NOT NULL,
  end_char INT NOT NULL,
  text_content TEXT NOT NULL,
  sha256_hash TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);*/

CREATE INDEX IF NOT EXISTS idx_chunks_run_id ON resume.chunks(run_id);
CREATE INDEX IF NOT EXISTS idx_chunks_source ON resume.chunks(source);