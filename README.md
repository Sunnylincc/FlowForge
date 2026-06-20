# FlowForge AI

FlowForge AI is a lightweight, open-source AI-assisted CI/CD platform for small teams, research labs, and indie developers. It imports repositories, detects simple project types, generates `.flowforge.yml`, runs pipeline steps locally in Docker containers, stores run history in SQLite, and includes a mock AI debugger that can be replaced with an OpenAI-backed provider later.

## MVP features

- Next.js App Router frontend with TypeScript, Tailwind CSS, and shadcn/ui-style primitives.
- FastAPI backend with SQLAlchemy and SQLite.
- GitHub repository import by URL or local path.
- Project detection for Node.js, Python, and Docker repositories.
- Generated YAML pipeline displayed in the UI.
- Local Docker CLI runner through Python subprocess.
- Pipeline runs, step statuses, logs, and timestamps stored in SQLite.
- Mock AI failure explanation provider with a clean replacement interface.
- Dashboard with projects, latest status, pipeline graph, logs, and AI diagnosis panel.

## Run locally

```bash
docker compose up
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

The compose setup mounts `/var/run/docker.sock` into the API container so the local runner can start step containers. See `docs/security.md` before running untrusted repositories.

## Import examples

From the UI, try importing one of these local paths:

- `/workspace/examples/node-app`
- `/workspace/examples/python-app`
- `/workspace/examples/docker-app`

## Repository layout

```text
apps/web          Next.js frontend
apps/api          FastAPI backend and Docker runner
packages/shared   Shared TypeScript types
examples          Tiny repositories for demos
docs              Architecture and security notes
```

## Production-hardening TODOs

- Move pipeline execution to isolated workers instead of the API process.
- Add authentication, authorization, and audit logs.
- Add resource limits, network policies, and per-run ephemeral workspaces.
- Validate and sign pipeline definitions before execution.
- Replace the mock AI provider with a configurable provider using secret management.
- Add background queues for long-running pipelines.
