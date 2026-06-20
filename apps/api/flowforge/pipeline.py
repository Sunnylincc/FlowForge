from pathlib import Path
import yaml

def detect_project_type(path: Path) -> str:
    types = []
    if (path / "package.json").exists(): types.append("node")
    if (path / "requirements.txt").exists() or (path / "pyproject.toml").exists(): types.append("python")
    if (path / "Dockerfile").exists(): types.append("docker")
    return "+".join(types) if types else "unknown"

def generate_pipeline(project_type: str) -> str:
    steps = [{"name": "checkout", "image": "alpine:3.20", "command": "echo Repository ready"}]
    if "node" in project_type:
        steps += [{"name": "install", "image": "node:20-alpine", "command": "npm install"}, {"name": "test", "image": "node:20-alpine", "command": "npm test -- --watch=false || npm test"}]
    if "python" in project_type:
        steps += [{"name": "install", "image": "python:3.12-slim", "command": "python -m pip install -r requirements.txt || true"}, {"name": "test", "image": "python:3.12-slim", "command": "python -m pytest || python -m unittest discover"}]
    if "docker" in project_type:
        steps += [{"name": "docker-build", "image": "docker:27-cli", "command": "docker build -t flowforge-local ."}]
    if project_type == "unknown":
        steps += [{"name": "inspect", "image": "alpine:3.20", "command": "find . -maxdepth 2 -type f | sort | head -50"}]
    return yaml.safe_dump({"version": 1, "name": "FlowForge generated pipeline", "steps": steps}, sort_keys=False)
