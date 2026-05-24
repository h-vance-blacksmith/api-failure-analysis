# API Failure Analysis

> **Production-style API failure lab with correlated logs, replayable incidents, and webhook debugging — designed to feed evidence into an AI triage copilot.**

Part of the [Ops Support Demo](https://github.com/h-vance/ops-support-demo) portfolio.

## Overview

A FastAPI-based failure simulation lab for diagnosing API failures in production environments. Includes seeded replayable incidents, structured JSON logging with trace IDs, webhook debugging, and an evidence bundle endpoint that feeds the [aws-bedrock-agent](https://github.com/h-vance/aws-bedrock-agent) triage copilot.

## Structure

```text
.
├── app/
│   ├── api.py                  # FastAPI with failure simulation + incidents
│   ├── incidents/
│   │   ├── models.py           # Pydantic: Incident, TimelineEvent, LogLine, RequestSample
│   │   └── store.py            # In-memory store, load from seeds/
│   ├── seeds/
│   │   ├── INC-001-auth-cascade.json
│   │   ├── INC-002-webhook-signature.json
│   │   └── INC-003-upstream-timeout.json
│   └── requirements.txt
├── scripts/
│   └── simulate-failures.sh    # Bash script for triggering failure scenarios
├── tests/
│   ├── conftest.py             # Pytest fixtures
│   └── test_endpoints.py       # Endpoint validation tests
├── infra/
│   └── k8s-deployment.yaml     # Kubernetes deployment manifest
└── Dockerfile                  # Container build
```

## Use Cases

- **Incident Triage:** Reproduce reported API failures in a controlled environment before escalating to engineering.
- **Pattern Recognition:** Reference seeded scenarios during live troubleshooting to identify known failure signatures.
- **Evidence Bundles:** Export structured incident JSON for engineering escalations and AI triage.

## Getting Started

```bash
pip install -r app/requirements.txt
python app/api.py
```

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `WEBHOOK_MODE` | `valid` | `valid`, `bad_signature`, or `slow_ack` |
| `SIMULATE_FLAKY_NETWORK` | `false` | Injects random latency |
| `EXTERNAL_DELAY_SECONDS` | `15` | Simulated upstream latency for `/api/v1/external-call` |
| `LOG_LEVEL` | `INFO` | Python log level (`DEBUG`, `INFO`, `WARNING`) |

Note: CORS is pre-configured to accept requests from `http://localhost:8080` and `http://127.0.0.1:8080` (the debug console). For production, update `allow_origins` in `app/api.py`.

Run tests:
```bash
pip install pytest httpx
pytest tests/
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/d/headers` | Echo inbound headers (debug teaching) |
| GET | `/metrics` | Request counters by status |
| POST | `/login` | Auth simulation (401) |
| GET | `/api/v1/data` | Protected data (401/403) |
| GET | `/api/v1/resource/{id}` | Resource lookup (404) |
| GET | `/api/v1/trigger-error` | Internal error (500) |
| GET | `/api/v1/external-call` | Upstream timeout simulation |
| GET | `/incidents` | List seeded incidents |
| GET | `/incidents/{id}` | Incident detail |
| POST | `/incidents/{id}/replay` | Re-execute incident curl steps |
| GET | `/incidents/{id}/evidence-bundle` | Structured JSON for triage copilot |
| POST | `/webhooks/inbound` | Accept webhook with optional HMAC validation |
| GET | `/webhooks/inbox` | List recent webhook deliveries |

## Related

- [aws-bedrock-agent](https://github.com/h-vance/aws-bedrock-ops-agent) — triage copilot over incident evidence ([live demo](https://aws-bedrock-ops-agent.onrender.com))
- [cloud-operations-runbook](https://github.com/h-vance/cloud-operations-runbook) — runbooks linked to each scenario
- [ops-support-demo](https://github.com/h-vance/ops-support-demo) — umbrella docker-compose demo

---
Maintained by Harrison Vance — Technical Support & Operations

## CORS

Both APIs include pre-configured `CORSMiddleware` allowing `http://localhost:8080` and `http://127.0.0.1:8080` (the debug console). Update `allow_origins` when deploying under a custom domain.
