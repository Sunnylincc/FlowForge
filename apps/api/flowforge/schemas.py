from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ImportProjectRequest(BaseModel):
    repo_url: str

class PipelineStepOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    run_id: int
    name: str
    command: str
    status: str
    logs: str
    started_at: datetime | None
    finished_at: datetime | None

class PipelineRunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_id: int
    status: str
    started_at: datetime | None
    finished_at: datetime | None
    steps: list[PipelineStepOut] = []

class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    repo_url: str
    project_type: str
    pipeline_yaml: str | None
    created_at: datetime
    runs: list[PipelineRunOut] = []

class DiagnosisOut(BaseModel):
    summary: str
    likely_cause: str
    suggested_fix: str
    provider: str = "mock"
