---
title: OpenEnv AIOps
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
license: mit
---
# AIOps Omni-Environment

## Overview
The AIOps Omni-Environment is a production-grade realistic benchmark for evaluating autonomous RL agents on critical operations (AIOps). Instead of evaluating simple games, the agent takes on the role of an SRE solving Tier-3 support desk operational tickets directly. 

## Real-world Utility
This environment solves for three distinct but crucial enterprise categories:
1. **FinOps (Cost Optimization)**: Identifying idle infrastructure and scaling it down safely.
2. **Data Governance**: Scrubbing Public PII leaks via database patching.
3. **Customer Ops**: Correctly identifying duplicate billing incidents and issuing real-time refunds via API interfaces.

## Task Descriptions (Difficulty scaled)
- **Easy (`task='easy'`)**: Issue a strict $50 API refund based on customer transaction ledgers.
- **Medium (`task='medium'`)**: Scan data buckets, sanitize a PII record down to `[REDACTED]` tokens while minimizing false positives/negatives.
- **Hard (`task='hard'`)**: Process heterogeneous compute metrics arrays to kill single `0%` CPU zombie nodes WITHOUT accidentally terminating `95%` CPU production nodes.

## Action & Observation Spaces
### Observation (AIOpsObservation)
Strict Pydantic models containing:
- `incident_description` (Trigger notification)
- `telemetry_output` (Stringified JSON payload returned from backend logic)

### Action (AIOpsAction)
Tool execution models containing:
- `command`: `str` specifying tools like `query_billing`, `terminate_node`, `patch_data`, `resolve`.
- `parameters`: `dict` mapping parameters like `{"node_id": "req-2"}` securely.

## Setup Instructions
```bash
pip install -r requirements.txt
python inference.py
```

## Running Docker
```bash
docker build -t openenv-aiops .
docker run -p 8000:8000 openenv-aiops
```

## Baseline Validation
The `inference.py` runs standard `gpt-4o-mini` evaluation across all 3 objectives producing 100% reproducibility natively. OpenEnv metadata handles Docker routing via FastApi (`server:app`).
