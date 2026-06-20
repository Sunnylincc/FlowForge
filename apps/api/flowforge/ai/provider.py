from abc import ABC, abstractmethod

class FailureExplainer(ABC):
    @abstractmethod
    def explain(self, logs: str) -> dict[str, str]: ...

class MockFailureExplainer(FailureExplainer):
    def explain(self, logs: str) -> dict[str, str]:
        lower = logs.lower()
        if "not found" in lower or "no such file" in lower:
            cause = "A command or required file appears to be missing in the build container."
            fix = "Check the generated pipeline image, install dependencies, and verify paths are relative to the repo root."
        elif "failed" in lower or "error" in lower:
            cause = "The step output contains an application or test failure."
            fix = "Open the failing step logs, reproduce the command locally, and patch the failing test or build script."
        else:
            cause = "No obvious failure signature was found in the logs."
            fix = "Review recent code changes and add more verbose logging to the failing step."
        return {"summary": "Mock AI diagnosis based on pipeline logs.", "likely_cause": cause, "suggested_fix": fix, "provider": "mock"}
