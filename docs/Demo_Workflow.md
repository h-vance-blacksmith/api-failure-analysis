# Demo Workflow

Follow this sequence when demoing the Ops Support Console:

## Symptom → Reproduce → Correlate → Escalate → Document

### 1. Symptom (the ticket)
A support ticket arrives: "Users can't access data — getting 401/403 errors after the maintenance window."

### 2. Reproduce (api-failure-analysis)
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1/data
# → 401: Authorization header missing

curl -s -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"wrong"}'
# → 401: Invalid credentials
```

### 3. Correlate (structured logs + trace IDs)
Check the incident timeline in the debug console:
- `GET /incidents/INC-001` — shows the full auth cascade
- Log lines include trace IDs linking each failed request
- Request samples show the progression: 401 → 401 → 403 → 200

### 4. Escalate (evidence bundle)
```bash
curl http://localhost:8000/incidents/INC-001/evidence-bundle | python3 -m json.tool
```
Export to the engineering ticket: includes timeline, log lines, request samples, and related endpoints.

### 5. Document (postmortem)
Reference [incident-postmortems](https://github.com/h-vance/incident-postmortems) template.
Link the [cloud-operations-runbook IAM runbook](https://github.com/h-vance/cloud-operations-runbook/blob/main/runbooks/identity/iam-access-denied.md).

## Scenario Reference

| Scenario | Trigger | What to Show |
| ---------- | --------- | ------------- |
| INC-001 | Missing/stale auth token | Timeline → logs → replay → evidence bundle |
| INC-002 | Webhook without HMAC signature | POST /webhooks/inbound → inspect inbox |
| INC-003 | Upstream timeout | long delay → client vs server mismatch |
