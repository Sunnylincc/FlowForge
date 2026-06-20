from pathlib import Path
import os, shutil, subprocess
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, selectinload
from .ai.provider import MockFailureExplainer
from .database import Base, engine, get_db
from .models import PipelineRun, Project
from .pipeline import detect_project_type, generate_pipeline
from .runner.docker_runner import run_pipeline
from .schemas import DiagnosisOut, ImportProjectRequest, PipelineRunOut, ProjectOut

Base.metadata.create_all(bind=engine)
app = FastAPI(title="FlowForge AI API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
WORKSPACE_ROOT = Path(os.getenv("WORKSPACE_ROOT", "./workspaces")); WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)

@app.get("/health")
def health(): return {"ok": True}

@app.post("/projects/import", response_model=ProjectOut)
def import_project(payload: ImportProjectRequest, db: Session = Depends(get_db)):
    repo_url = payload.repo_url.strip(); name = Path(repo_url.rstrip("/")).stem.replace(".git", "") or "project"
    dest = WORKSPACE_ROOT / f"{name}-{abs(hash(repo_url)) % 100000}"
    if dest.exists(): shutil.rmtree(dest)
    if repo_url.startswith("http") or repo_url.endswith(".git"):
        subprocess.run(["git", "clone", "--depth", "1", repo_url, str(dest)], check=True, capture_output=True, text=True, timeout=120)
    else:
        shutil.copytree(Path(repo_url).expanduser().resolve(), dest)
    project_type = detect_project_type(dest); pipeline_yaml = generate_pipeline(project_type)
    (dest / ".flowforge.yml").write_text(pipeline_yaml)
    project = Project(name=name, repo_url=repo_url, local_path=str(dest), project_type=project_type, pipeline_yaml=pipeline_yaml)
    db.add(project); db.commit(); db.refresh(project)
    return project

@app.get("/projects", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).options(selectinload(Project.runs).selectinload(PipelineRun.steps)).order_by(Project.created_at.desc()).all()

@app.get("/projects/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).options(selectinload(Project.runs).selectinload(PipelineRun.steps)).get(project_id)
    if not project: raise HTTPException(404, "Project not found")
    return project

@app.post("/projects/{project_id}/generate-pipeline", response_model=ProjectOut)
def refresh_pipeline(project_id: int, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project: raise HTTPException(404, "Project not found")
    project.project_type = detect_project_type(Path(project.local_path)); project.pipeline_yaml = generate_pipeline(project.project_type)
    Path(project.local_path, ".flowforge.yml").write_text(project.pipeline_yaml); db.commit(); db.refresh(project)
    return project

@app.post("/projects/{project_id}/runs", response_model=PipelineRunOut)
def create_run(project_id: int, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project: raise HTTPException(404, "Project not found")
    run = PipelineRun(project_id=project.id, status="queued"); db.add(run); db.commit(); db.refresh(run)
    return run_pipeline(db, run, project.local_path, project.pipeline_yaml or generate_pipeline(project.project_type))

@app.get("/runs/{run_id}", response_model=PipelineRunOut)
def get_run(run_id: int, db: Session = Depends(get_db)):
    run = db.query(PipelineRun).options(selectinload(PipelineRun.steps)).get(run_id)
    if not run: raise HTTPException(404, "Run not found")
    return run

@app.get("/runs/{run_id}/logs")
def get_logs(run_id: int, db: Session = Depends(get_db)):
    run = db.query(PipelineRun).options(selectinload(PipelineRun.steps)).get(run_id)
    if not run: raise HTTPException(404, "Run not found")
    return {"run_id": run_id, "logs": "\n\n".join(f"## {s.name}\n{s.logs}" for s in run.steps)}

@app.post("/runs/{run_id}/ai-diagnose", response_model=DiagnosisOut)
def diagnose(run_id: int, db: Session = Depends(get_db)):
    run = db.query(PipelineRun).options(selectinload(PipelineRun.steps)).get(run_id)
    if not run: raise HTTPException(404, "Run not found")
    return MockFailureExplainer().explain("\n".join(s.logs for s in run.steps))
