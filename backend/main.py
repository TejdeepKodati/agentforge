"""
AgentForge FastAPI Server.
Provides REST and telemetry endpoints for multi-agent code orchestration and automated quality gates.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from core.orchestrator import MultiAgentOrchestrator

app = FastAPI(
    title="AgentForge Multi-Agent AI Code Orchestration API",
    version="1.0.0",
    description="Production-grade multi-agent engine for intent prompting, AST security auditing, unit test synthesis, and LLMOps telemetry."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = MultiAgentOrchestrator()


class OrchestrateRequest(BaseModel):
    prompt: str
    target_language: Optional[str] = "python"


PRESETS = [
    {
        "id": "lru-cache-cpp",
        "title": "Thread-Safe LRU Cache (C++20)",
        "prompt": "Design a high-performance thread-safe LRU cache in C++ with std::unordered_map, std::list, and std::shared_mutex for O(1) operations.",
        "language": "cpp",
        "tag": "Systems & DSA"
    },
    {
        "id": "lru-cache-python",
        "title": "Thread-Safe LRU Cache (Python)",
        "prompt": "Implement a high-throughput thread-safe LRU Cache in Python using a doubly linked list, hash map, and reentrant locks with O(1) get and put.",
        "language": "python",
        "tag": "Data Structures"
    },
    {
        "id": "rate-limiter",
        "title": "Sliding Window Rate Limiter",
        "prompt": "Implement a thread-safe sliding window log distributed rate limiter to enforce API quotas and prevent boundary burst exploitation.",
        "language": "python",
        "tag": "Distributed Systems"
    },
    {
        "id": "jwt-validator",
        "title": "Microservice HMAC-SHA256 Token Validator",
        "prompt": "Build an auditable cryptographic JWT Bearer Token validator with HMAC-SHA256 signature verification, expiry validation, and claim decoding.",
        "language": "python",
        "tag": "Security & Auth"
    }
]


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AgentForge Orchestration Engine",
        "version": "1.0.0",
        "active_agents": ["Planner", "Generator", "SecurityAuditor", "TestRunner", "Synthesizer"]
    }


@app.get("/api/presets")
def get_presets():
    return {"presets": PRESETS}


@app.post("/api/orchestrate")
def run_orchestration(req: OrchestrateRequest):
    if not req.prompt or not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    result = orchestrator.run_pipeline(prompt=req.prompt, target_language=req.target_language or "python")
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
