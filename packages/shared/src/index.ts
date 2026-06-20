export type RunStatus = "queued" | "running" | "success" | "failed";
export type PipelineStep = { id: number; name: string; command: string; status: RunStatus; logs: string; started_at?: string; finished_at?: string };
export type PipelineRun = { id: number; project_id: number; status: RunStatus; started_at?: string; finished_at?: string; steps: PipelineStep[] };
export type Project = { id: number; name: string; repo_url: string; project_type: string; pipeline_yaml?: string; created_at: string; runs: PipelineRun[] };
