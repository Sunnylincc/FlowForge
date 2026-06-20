from datetime import datetime
from pathlib import Path
import subprocess, yaml
from sqlalchemy.orm import Session
from ..models import PipelineRun, PipelineStep

def run_pipeline(db: Session, run: PipelineRun, repo_path: str, pipeline_yaml: str) -> PipelineRun:
    spec = yaml.safe_load(pipeline_yaml) or {}
    run.status = "running"; run.started_at = datetime.utcnow(); db.commit()
    failed = False
    for item in spec.get("steps", []):
        step = PipelineStep(run_id=run.id, name=item["name"], command=item["command"], status="running", started_at=datetime.utcnow())
        db.add(step); db.commit(); db.refresh(step)
        image = item.get("image", "alpine:3.20")
        cmd = ["docker", "run", "--rm", "-v", f"{Path(repo_path).resolve()}:/workspace", "-w", "/workspace", image, "sh", "-lc", item["command"]]
        # TODO: production hardening: add resource limits, network controls, non-root users, and isolated workers.
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=900)
        step.logs = (proc.stdout or "") + (proc.stderr or "")
        step.status = "success" if proc.returncode == 0 else "failed"
        step.finished_at = datetime.utcnow(); db.commit()
        if proc.returncode != 0:
            failed = True; break
    run.status = "failed" if failed else "success"
    run.finished_at = datetime.utcnow(); db.commit(); db.refresh(run)
    return run
