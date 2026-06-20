# Security notes

FlowForge AI runs repository commands in Docker containers, but the MVP is **not a secure sandbox** for untrusted code.

## Key risks

- The API container mounts the host Docker socket in `docker-compose.yml`. Code with Docker access can often gain host-level control.
- Pipeline commands may exfiltrate secrets available in the environment or network.
- The MVP does not enforce CPU, memory, disk, process, or network limits.
- The MVP does not authenticate users or isolate tenants.
- Imported repositories and generated pipelines are not cryptographically verified.

## Current mitigations

- Steps run in short-lived containers with the repository mounted as a workspace.
- The generated pipeline is simple and visible before execution.
- The AI debugger is a mock provider and does not send logs to external services.

## Production-hardening TODOs

- Use isolated runner hosts or microVMs instead of mounting the Docker socket into the API service.
- Run containers as non-root with read-only filesystems where possible.
- Apply strict CPU, memory, disk, timeout, and network policies.
- Store secrets in a dedicated secret manager and inject them only into approved steps.
- Add authentication, authorization, organization boundaries, and audit logging.
- Add allowlists for images and commands, plus repository trust policies.
- Review logs for sensitive values before storing or sending them to an AI provider.
