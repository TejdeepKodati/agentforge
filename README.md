# AgentForge: Multi-Agent AI Code Orchestration & Quality Gate Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14.2-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg)](https://www.typescriptlang.org/)

**AgentForge** is an enterprise-grade multi-agent autonomous engineering platform designed to orchestrate intent prompting, algorithmic synthesis, AST-level static security auditing, sandboxed dynamic test execution, and real-time LLMOps observability.

The platform simulates a lean engineering pod architecture where specialized agents autonomously collaborate to translate high-level technical specifications into verified, production-ready code with automated CI/CD deployment gate verdicts.

---

## 🏛 Architecture Overview

```
                      +-----------------------------+
                      |     User Intent Prompt      |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      | Input Guardrail & Sanitizer |
                      |   (PII / Injection Check)   |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |    1. Intent Planner Agent  |
                      | (Task Deconstruction / DSA) |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |   2. Code Generator Agent   |
                      |  (C++20 / Python / Typing)  |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |  3. AST Security Auditor    |
                      | (Static AST / CVE Scans)    |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |    4. Sandbox Test Runner   |
                      | (Edge Case Assertion Check) |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |  5. Pod Synthesizer Agent   |
                      | (Gate Verdict: PASS/BLOCK)  |
                      +--------------+--------------+
                                     |
                                     v
            +-----------------------------------------------+
            |         LLMOps Observability Telemetry         |
            | Latency (ms) | Tokens | Est. Cost | Risk Score|
            +-----------------------------------------------+
```

---

## ✨ Key Features & Capabilities

1. **Multi-Agent Pod Orchestration**:
   - **Intent Planner Agent**: Deconstructs requirements into concrete architectural blueprints, target time/space complexities, required data structures, and edge-case catalogs.
   - **Code Generator Agent**: Synthesizes type-annotated, idiomatic code supporting modern **C++20** (RAII, `std::shared_mutex`, `std::list`, `std::unordered_map`) and **Python 3.12** (thread safety, sentinels, clean abstraction).
   - **AST Security Auditor Agent**: Performs deep Abstract Syntax Tree inspection, detecting dangerous primitives (`eval`, `exec`, shell executions), cyclomatic complexity, and credential leakage.
   - **Automated Test Runner**: Dynamically generates targeted test suites with edge cases, executing them within an isolated sandbox runner.
   - **Pod Synthesizer Agent**: Computes a formal Quality Gate verdict (`PASSED`, `CONDITIONAL_APPROVAL`, or `BLOCKED`) with actionable deployment recommendations.

2. **LLMOps Observability & Guardrails**:
   - **Real-Time Telemetry**: Granular latency breakdown per agent phase (ms), token accounting (prompt, completion, total), and dynamic inference cost estimation.
   - **Hallucination & Drift Risk Scoring**: Multi-factor objective score based on AST validity, test assertion results, and security findings.
   - **Prompt Injection & PII Guardrails**: Pre-execution regex and semantic filters intercepting jailbreak attempts and masking sensitive keys/emails.

3. **Interactive Next.js Dashboard**:
   - Visual execution pipeline with live agent status progression.
   - Tabbed workspace for Source Code, Architectural Blueprint, AST Security Findings, and Test Assertions.
   - One-click presets for Thread-Safe LRU Cache (C++20), Thread-Safe LRU Cache (Python), Distributed Sliding Window Rate Limiter, and Cryptographic JWT Bearer Validator.

---

## 🛠 Tech Stack

- **Backend / Core Engine**: Python 3.12, FastAPI, Pydantic v2, AST, Uvicorn, Pytest
- **Frontend / Dashboard**: Next.js 14, React 18, TypeScript, Tailwind CSS, Lucide Icons
- **DevOps & Containers**: Docker, Docker Compose, Vercel

---

## 🚀 Getting Started

### Local Setup (Backend)

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run automated tests
pytest tests -v

# Start FastAPI server
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000` with interactive Swagger docs at `http://localhost:8000/docs`.

### Local Setup (Frontend)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Open `http://localhost:3000` in your browser.

---

## 🧪 Automated Testing

AgentForge includes comprehensive unit tests verifying agent behaviors, guardrail filtering, AST safety scanning, and end-to-end orchestration pipelines:

```bash
pytest backend/tests/test_agentforge.py -v
```

---

## 📄 License

This project is licensed under the MIT License.
