# FlowForge AI architecture

FlowForge AI is a small monorepo with three primary layers:

1. **Web app (`apps/web`)**: a Next.js App Router dashboard. It renders the landing page, projects list, project details, run details, pipeline graph, logs, and the AI debugger panel. Mock project data keeps the UI useful when the API has not imported a repository yet.
2. **API (`apps/api`)**: a FastAPI service with SQLAlchemy models for projects, runs, and steps. It imports repositories, detects project types, generates YAML, starts runs, returns logs, and delegates failure explanations to an AI provider interface.
3. **Runner (`apps/api/flowforge/runner`)**: a minimal Docker CLI runner. Each pipeline step runs as `docker run --rm` with the repository mounted at `/workspace`.

## Data model

- `Project`: repository metadata, detected type, local path, generated YAML, creation time.
- `PipelineRun`: status and timestamps for a project run.
- `PipelineStep`: command, logs, status, and timestamps for one run step.

## Pipeline generation

Project type detection is intentionally simple:

- `package.json` => Node.js
- `requirements.txt` or `pyproject.toml` => Python
- `Dockerfile` => Docker

The API writes the generated YAML to `.flowforge.yml` inside the imported workspace and stores a copy in SQLite for display.

## AI provider boundary

`FailureExplainer` is an abstract provider interface. The MVP includes `MockFailureExplainer`, which uses log heuristics. A future OpenAI provider can implement the same interface without changing API routes or UI contracts.

## Local development flow

1. `docker compose up` starts API and web services.
2. A user imports a repository URL or local path.
3. The API clones or copies the repo into the workspace directory.
4. The API detects the stack and generates `.flowforge.yml`.
5. The user starts a run.
6. The runner executes steps with Docker and persists logs/statuses.
7. The UI displays results and can request an AI diagnosis.
