---
title: OpenEnv AIOps
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
license: mit
---

# 🌐 Enterprise AIOps Omni-Environment

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/purvansh01/openenv-aiops)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A production-grade, highly-deterministic OpenEnv sandbox designed to evaluate autonomous agents on complex, real-world Cloud Infrastructure, FinOps, and Data Governance workflows.**

---

## 🎯 The Vision: Beyond "Toy Problems"
The Reinforcement Learning ecosystem suffers from an oversaturation of "toy problems" (e.g., Tic-Tac-Toe, Wordle, block-stacking). While these are useful for fundamental agent training, they fail to benchmark an LLM's capacity in high-stakes, real-world enterprise environments.

The **Enterprise AIOps Omni-Environment** bridges this gap. It drops the AI agent into the seat of a Tier-3 Site Reliability Engineer (SRE) handling live IT alert tickets.

### Real-World Utility Domains:
1. **FinOps (Cost Optimization):** Agents must securely identify and terminate idle data center compute nodes without risking production uptime.
2. **Data Governance (Compliance):** Agents must detect PII/PHI (Protected Health Information) leaks in a mock database and securely sanitize the payloads programmatically.
3. **Customer Operations:** Agents are deployed to investigate cross-referenced CRM billing ledgers to process exact-dollar dynamic refunds via an API interface.

---

## 🏗️ OpenEnv Architecture

This repository strictly implements the **OpenEnv (`openenv-core`) Protocol**, deploying a lightweight, standalone `FastAPI` instance fully containerized for Hugging Face Spaces.

- **Strict Type Safety:** Driven by Pydantic models (`AIOpsAction`, `AIOpsObservation`), ensuring robust validation of agent inputs.
- **RESTful Endpoints:** Exposes compliant `/reset`, `/step`, and `/state` operations matching Hugging Face evaluation architectures.
- **Stateless Stability:** `max_concurrent_envs=1` configured securely mitigating `openenv` wrapper collisions over WebSocket/HTTP routing.
- **HF Native Container:** Executes as non-root `user 1000` via a stripped-down `Python 3.10-slim` Debian build over Port `7860`.

---

## 🚀 Tasks & Deterministic Grading

Unlike heuristic string-matching or unpredictable LLM-as-a-Judge evaluations, this environment utilizes programmatic grading schemas. Agents earn fractional rewards (`0.0 - 1.0` range bounds) for progressive actions and hard penalties (`-1.0`) for catastrophic operational failures.

| Difficulty | Task Domain | Objective | Reward Schema |
| :--- | :--- | :--- | :--- |
| **Easy** | CRM Ops | Query a user's ledger -> Identify duplicate transaction -> Refund $50 API call. | `+0.8` (Refund Sent), `+0.2` (Resolve Ticket), `-0.5` (Wrong Refund). |
| **Medium**| Data Gov | Locate PHI String -> Patch record via regex-style sanitization to `[REDACTED]`. | `+0.8` (Data Sanitized), `+0.2` (Resolve Ticket), `-0.5` (Missed PII). |
| **Hard** | FinOps | Analyze Fleet array -> Detect `0%` CPU node -> `terminate_node("node-2")`. | `+0.8` (Node Terminated), `+0.2` (Resolve), `-1.0` (Kill Production). |

---

## ⚙️ Submission Toolkit

### Evaluation Script
The root contains the `inference.py` evaluator baseline. It is mapped to automatically orchestrate across the agent objectives using `OpenAI` client tools.
- Strict mapping to STDOUT specifications: `[START]`, `[STEP]`, and `[END]`.

### Local Testing
```bash
pip install -r requirements.txt
python inference.py
```

### Docker Manual Boot
```bash
docker build -t openenv-aiops .
docker run -p 8000:7860 openenv-aiops
```

---
*Built for the Meta OpenEnv Agentic AI Hackathon.*
