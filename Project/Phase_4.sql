/*CREATE TABLE IF NOT EXISTS resume.run_logs (
  log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id UUID NOT NULL REFERENCES resume.runs(run_id) ON DELETE CASCADE,
  stage TEXT NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);*/

CREATE INDEX IF NOT EXISTS idx_run_logs_run_id ON resume.run_logs(run_id);
CREATE INDEX IF NOT EXISTS idx_run_logs_stage ON resume.run_logs(stage);

